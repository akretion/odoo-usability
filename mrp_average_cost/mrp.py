# -*- coding: utf-8 -*-
# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from odoo.tools import float_compare, float_is_zero
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
        "the BOM in the unit of measure of the BOM, in company currency. "
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
        help="Total Cost for the production of the quantity of the BOM "
        "in the unit of measure of the BOM in company currency. Total Cost = "
        "Total Components Cost + Total Labour Cost + Extra Cost")

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
            pt.write({'standard_price': self.total_cost})
            logger.info(
                'Cost price updated to %s on product %s',
                self.total_cost, pt.display_name)
        return

    @api.model
    def _phantom_update_product_standard_price(self):
        '''Called by cron'''
        logger.info(
            'Start automatic update of cost price of phantom bom products')
        boms = self.env['mrp.bom'].search([('type', '=', 'phantom')])
        for bom in boms:
            bom.manual_update_product_standard_price()
        logger.info(
            'End automatic update of cost price of phantom bom products')
        return True


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    # In v10, don't put a property field as related field
    # because it won't have the right value in multi-company context
    standard_price = fields.Float(
        compute='_compute_standard_price', readonly=True)
    company_currency_id = fields.Many2one(
        related='bom_id.company_id.currency_id', readonly=True,
        string='Company Currency')

    def _compute_standard_price(self):
        for line in self:
            line.standard_price = line.product_id.standard_price


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

    def _generate_finished_moves(self):
        move = super(MrpProduction, self)._generate_finished_moves()
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        if (
                self.bom_id and
                not float_is_zero(
                    self.bom_id.product_qty, precision_digits=prec)):
            unit_cost_bom_uom =\
                self.bom_id.total_cost / self.bom_id.product_qty
            unit_cost_mo_uom = self.bom_id.product_uom_id._compute_quantity(
                unit_cost_bom_uom, self.product_uom_id, round=False)
            # MO and finished move are in the same UoM
            move.write({'price_unit': unit_cost_mo_uom})
            self.write({'unit_cost': unit_cost_mo_uom})
        return move

    # No need to write directly on standard_price of product
    # the method product_price_update_after_done of stock.move
    # located in stock_account does the job for us
