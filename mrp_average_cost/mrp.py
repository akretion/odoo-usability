# -*- coding: utf-8 -*-
# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare
import logging

logger = logging.getLogger(__name__)


class LabourCostProfile(models.Model):
    _name = 'labour.cost.profile'
    _inherit = ['mail.thread']
    _description = 'Labour Cost Profile'

    name = fields.Char(
        string='Name', required=True, track_visibility='onchange')
    hour_cost = fields.Float(
        string='Cost per Hour', required=True,
        digits=dp.get_precision('Product Price'),
        track_visibility='onchange',
        help="Labour cost per hour per person in company currency")
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'labour.cost.profile'))
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, u'%s (%s %s)' % (
                record.name, record.hour_cost,
                record.company_currency_id.symbol)))
        return res


class MrpBomLabourLine(models.Model):
    _name = 'mrp.bom.labour.line'
    _description = 'Labour lines on BOM'

    bom_id = fields.Many2one(
        'mrp.bom', string='Labour Lines', ondelete='cascade')
    labour_time = fields.Float(
        string='Labour Time', required=True,
        digits=dp.get_precision('Labour Hours'),
        help="Average labour time for the production of "
        "items of the BOM, in hours.")
    labour_cost_profile_id = fields.Many2one(
        'labour.cost.profile', string='Labour Cost Profile', required=True)
    labour_cost_subtotal = fields.Float(
        compute='_compute_labour_cost_subtotal', readonly=True, store=True,
        digits=dp.get_precision('Product Price'), string='Subtotal')
    company_currency_id = fields.Many2one(
        related='bom_id.company_id.currency_id', readonly=True,
        string='Company Currency')
    note = fields.Text('Note')

    _sql_constraints = [(
        'labour_time_positive',
        'CHECK (labour_time >= 0)',
        "The value of the field 'Labour Time' must be positive or 0.")]

    @api.depends('labour_time', 'labour_cost_profile_id.hour_cost')
    def _compute_labour_cost_subtotal(self):
        for line in self:
            subtotal = line.labour_time * line.labour_cost_profile_id.hour_cost
            line.labour_cost_subtotal = subtotal


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.depends('labour_line_ids.labour_cost_subtotal')
    def _compute_total_labour_cost(self):
        for bom in self:
            cost = 0.0
            for lline in bom.labour_line_ids:
                cost += lline.labour_cost_subtotal
            bom.total_labour_cost = cost

    @api.depends(
        'bom_line_ids.product_id.standard_price',
        'bom_line_ids.product_uom_id', 'extra_cost', 'total_labour_cost')
    def _compute_total_cost(self):
        for bom in self:
            component_cost = 0.0
            for line in bom.bom_line_ids:
                component_price = line.product_id.standard_price
                component_qty_product_uom =\
                    line.product_uom_id._compute_quantity(
                        line.product_qty, line.product_id.uom_id)
                component_cost += component_price * component_qty_product_uom
            total_cost =\
                component_cost + bom.extra_cost + bom.total_labour_cost
            bom.total_components_cost = component_cost
            bom.total_cost = total_cost

    labour_line_ids = fields.One2many(
        'mrp.bom.labour.line', 'bom_id', string='Labour Lines')
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')
    total_labour_cost = fields.Float(
        compute='_compute_total_labour_cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        string="Total Labour Cost")
    extra_cost = fields.Float(
        string='Extra Cost', track_visibility='onchange',
        digits=dp.get_precision('Product Price'),
        help="Extra cost for the production of the quantity of "
        "items of the BOM, in company currency. "
        "You can use this field to enter the cost of the consumables "
        "that are used to produce the product but are not listed in "
        "the BOM")
    total_components_cost = fields.Float(
        compute='_compute_total_cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        string='Total Components Cost')
    total_cost = fields.Float(
        compute='_compute_total_cost', readonly=True, string='Total Cost',
        digits=dp.get_precision('Product Price'),
        help="Total Cost = Total Components Cost + "
        "Total Labour Cost + Extra Cost")

    def manual_update_product_standard_price(self):
        self.ensure_one()
        if 'product_price_history_origin' not in self._context:
            self = self.with_context(
                product_price_history_origin='Manual update from BOM')
        precision = self.env['decimal.precision'].precision_get(
            'Product Price')
        pt = self.product_tmpl_id
        if float_compare(
                pt.standard_price, self.total_cost,
                precision_digits=precision):
            pt.standard_price = self.total_cost
            logger.info(
                'Cost price updated to %s on product %s',
                self.total_cost, pt.display_name)
        return

    @api.model
    def _phantom_update_product_standard_price(self):
        '''Called by cron'''
        logger.info(
            'Start automatic update of cost price of phantom bom products')
        origin = 'Automatic update of Phantom BOMs'
        boms = self.env['mrp.bom'].search([('type', '=', 'phantom')])
        for bom in boms:
            bom.with_context(product_price_history_origin=origin).\
                manual_update_product_standard_price()
        logger.info(
            'End automatic update of cost price of phantom bom products')
        return True


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    standard_price = fields.Float(
        related='product_id.standard_price', readonly=True)
    company_currency_id = fields.Many2one(
        related='bom_id.company_id.currency_id', readonly=True,
        string='Company Currency')


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    unit_cost = fields.Float(
        string='Unit Cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        help="This cost per unit in the unit of measure of the product "
        "in company currency takes into account "
        "the cost of the raw materials and the labour cost defined on"
        "the BOM.")
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')

    def compute_order_unit_cost(self):
        self.ensure_one()
        mo_total_price = 0.0  # In the UoM of the M0
        labor_cost_per_unit = 0.0  # In the UoM of the product
        extra_cost_per_unit = 0.0  # In the UoM of the product
        # I read the raw materials MO, not on BOM, in order to make
        # it work with the "dynamic" BOMs (few raw material are auto-added
        # on the fly on MO)
        for raw_smove in self.move_raw_ids:
            # I don't filter on state, in order to make it work with
            # partial productions
            # For partial productions, mo.product_qty is not updated
            # so we compute with fully qty and we compute with all raw
            # materials (consumed or not), so it gives a good price
            # per unit at the end
            raw_price = raw_smove.product_id.standard_price
            raw_qty_product_uom = raw_smove.product_uom._compute_quantity(
                raw_smove.product_qty,
                raw_smove.product_id.uom_id)
            raw_material_cost = raw_price * raw_qty_product_uom
            logger.info(
                'MO %s product %s: raw_material_cost=%s',
                self.name, raw_smove.product_id.name, raw_material_cost)
            mo_total_price += raw_material_cost
        if self.bom_id:
            bom = self.bom_id
            if not bom.product_qty:
                raise UserError(_(
                    "Missing Product Quantity on bill of material '%s'.")
                    % bom.name)
            bom_qty_product_uom = bom.product_uom_id._compute_quantity(
                bom.product_qty, bom.product_tmpl_id.uom_id)
            assert bom_qty_product_uom > 0, 'BoM qty should be positive'
            labor_cost_per_unit = bom.total_labour_cost / bom_qty_product_uom
            extra_cost_per_unit = bom.extra_cost / bom_qty_product_uom
        # mo_standard_price and labor_cost_per_unit are
        # in the UoM of the product (not of the MO/BOM)
        mo_qty_product_uom = self.product_uom_id._compute_quantity(
            self.product_qty, self.product_id.uom_id)
        assert mo_qty_product_uom > 0, 'MO qty should be positive'
        mo_standard_price = mo_total_price / mo_qty_product_uom
        logger.info(
            'MO %s: labor_cost_per_unit=%s', self.name, labor_cost_per_unit)
        logger.info(
            'MO %s: extra_cost_per_unit=%s', self.name, extra_cost_per_unit)
        mo_standard_price += labor_cost_per_unit
        mo_standard_price += extra_cost_per_unit
        self.write({'unit_cost': mo_standard_price})
        logger.info('MO %s: unit_cost=%s', self.name, mo_standard_price)
        return mo_standard_price

    def update_standard_price(self):
        self.ensure_one()
        product = self.product_id
        mo_standard_price = self.compute_order_unit_cost()
        mo_qty_product_uom = self.product_uom_id._compute_quantity(
            self.product_qty, self.product_id.uom_id)
        # I can't use the native method _update_average_price of stock.move
        # because it only works on move.picking_id.type == 'in'
        # As we do the super() at the END of this method,
        # the qty produced by this MO in NOT counted inside
        # product.qty_available
        qty_before_mo = product.qty_available
        logger.info(
            'MO %s product %s: standard_price before production: %s',
            self.name, product.name, product.standard_price)
        logger.info(
            'MO %s product %s: qty before production: %s',
            self.name, product.name, qty_before_mo)
        # Here, we handle as if we were in v8 (!)
        # so we consider that standard_price is in company currency
        # It will not work if you are in multi-company environment
        # with companies in different currencies
        new_std_price = (
            (product.standard_price * qty_before_mo) +
            (mo_standard_price * mo_qty_product_uom)) / \
            (qty_before_mo + mo_qty_product_uom)
        origin = _(
            '%s (Qty before: %s - Added qty: %s - Unit price of '
            'added qty: %s)') % (
            self.name, qty_before_mo, mo_qty_product_uom, mo_standard_price)
        product.with_context(product_price_history_origin=origin).write(
            {'standard_price': new_std_price})
        logger.info(
            'MO %s product %s: standard_price updated to %s',
            self.name, product.name, new_std_price)
        return True

    def button_mark_done(self):
        self.ensure_one()
        # cost_method is a compute field that gets the value from product
        # or, if empty, from the product category
        if self.product_id.cost_method == 'average':
            self.update_standard_price()
        return super(MrpProduction, self).button_mark_done()
