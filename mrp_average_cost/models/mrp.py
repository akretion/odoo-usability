# Copyright (C) 2016-2024 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools import float_compare
import logging

logger = logging.getLogger(__name__)


class MrpBomLabourLine(models.Model):
    _name = 'mrp.bom.labour.line'
    _description = 'Labour lines on BOM'

    bom_id = fields.Many2one(
        comodel_name='mrp.bom',
        string='Bill of Material',
        ondelete='cascade')
    labour_time = fields.Float(
        string='Labour Time',
        required=True,
        digits='Labour Hours',
        help="Average labour time for the production of "
             "items of the BOM, in hours.")
    labour_cost_profile_id = fields.Many2one(
        comodel_name='labour.cost.profile',
        string='Labour Cost Profile',
        required=True)
    note = fields.Text()

    _sql_constraints = [(
        'labour_time_positive',
        'CHECK (labour_time >= 0)',
        "The value of the field 'Labour Time' must be positive or 0.")]


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    labour_line_ids = fields.One2many(
        'mrp.bom.labour.line', 'bom_id', string='Labour Lines')
    total_labour_cost = fields.Float(
        compute='_compute_total_labour_cost', digits='Product Price', store=True)
    extra_cost = fields.Float(
        tracking=True, digits='Product Price',
        help="Extra cost for the production of the quantity of "
        "items of the BOM, in company currency. "
        "You can use this field to enter the cost of the consumables "
        "that are used to produce the product but are not listed in "
        "the BOM")
    total_components_cost = fields.Float(
        compute='_compute_total_cost', digits='Product Price')
    total_cost = fields.Float(
        compute='_compute_total_cost', digits='Product Price',
        help="Total cost for the quantity and unit of measure of the bill of material. "
        "Total Cost = Total Components Cost + Total Labour Cost + Extra Cost")
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', string='Company Currency')

    @api.depends(
        'labour_line_ids.labour_time',
        'labour_line_ids.labour_cost_profile_id.hour_cost')
    def _compute_total_labour_cost(self):
        for bom in self:
            cost = 0.0
            for lline in bom.labour_line_ids:
                cost += lline.labour_time *\
                    lline.labour_cost_profile_id.hour_cost
            bom.total_labour_cost = cost

    @api.depends(
        'bom_line_ids.product_id.standard_price',
        'total_labour_cost', 'extra_cost')
    def _compute_total_cost(self):
        for bom in self:
            comp_cost = 0.0
            for line in bom.bom_line_ids:
                comp_price = line.product_id.standard_price
                comp_qty_product_uom = line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id)
                comp_cost += comp_price * comp_qty_product_uom
            total_cost = comp_cost + bom.extra_cost + bom.total_labour_cost
            bom.total_components_cost = comp_cost
            bom.total_cost = total_cost

    @api.model
    def _phantom_update_product_standard_price(self):
        logger.info('Start to auto-update cost price from phantom boms')
        boms = self.search([('type', '=', 'phantom')])
        boms.manual_update_product_standard_price()
        logger.info('End of the auto-update cost price from phantom boms')

    def manual_update_product_standard_price(self):
        prec = self.env['decimal.precision'].precision_get(
            'Product Price')
        for bom in self:
            if bom.product_id:
                products = bom.product_id
            else:
                products = bom.product_tmpl_id.product_variant_ids
            for product in products:
                standard_price = product._compute_bom_price(bom)
                if float_compare(product.standard_price, standard_price, precision_digits=prec):
                    product.write({'standard_price': standard_price})
                    logger.info(
                        'Cost price updated to %s on product %s',
                        standard_price, product.display_name)


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    standard_price = fields.Float(related='product_id.standard_price')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_bom_price(self, bom, boms_to_recompute=False):
        # Native method of mrp_account
        # WARNING dirty hack ; I hope it doesn't break too many things
        self.ensure_one()
        bom_cost_per_unit_in_product_uom = 0
        qty_product_uom = bom.product_uom_id._compute_quantity(bom.product_qty, self.uom_id)
        if qty_product_uom:
            bom_cost_per_unit_in_product_uom = bom.total_cost / qty_product_uom
        return bom_cost_per_unit_in_product_uom


class LabourCostProfile(models.Model):
    _name = 'labour.cost.profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Labour Cost Profile'

    name = fields.Char(
        required=True,
        tracking=True)
    hour_cost = fields.Float(
        string='Cost per Hour',
        required=True,
        digits='Product Price',
        tracking=True,
        help="Labour cost per hour per person in company currency")

    company_id = fields.Many2one(
        comodel_name='res.company', required=True,
        default=lambda self: self.env.company)

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', store=True, string='Company Currency')

    @api.depends('name', 'hour_cost', 'company_currency_id.symbol')
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, '%s (%s %s)' % (
                record.name, record.hour_cost,
                record.company_currency_id.symbol)))
        return res


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', string='Company Currency')
    # extra_cost is per unit in the UoM of the mrp.production (product_uom_id)
    extra_cost = fields.Float(
        compute='_compute_extra_cost', store=True, readonly=False,
        help="For a regular production order, it takes into account the labor cost "
        "and the extra cost defined on the bill of material.")

    # Strategy for v14 : we write labor costs and bom's extra cost on the native field extra_cost
    # of mrp.production => it is automatically added by the code of mrp_account

    @api.depends('bom_id', 'product_id')
    def _compute_extra_cost(self):
        for prod in self:
            bom = prod.bom_id
            if bom and bom.type == 'normal':
                extra_cost_bom_qty_uom = bom.extra_cost + bom.total_labour_cost
                extra_cost_per_unit_in_prod_uom = 0
                qty_prod_uom = bom.product_uom_id._compute_quantity(bom.product_qty, prod.product_uom_id)
                if qty_prod_uom:
                    extra_cost_per_unit_in_prod_uom = extra_cost_bom_qty_uom / qty_prod_uom
                prod.extra_cost = extra_cost_per_unit_in_prod_uom
