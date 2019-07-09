# -*- coding: utf-8 -*-
# Copyright (C) 2016-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from odoo.tools import float_compare, float_is_zero
import logging

logger = logging.getLogger(__name__)


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
    note = fields.Text(string='Note')

    _sql_constraints = [(
        'labour_time_positive',
        'CHECK (labour_time >= 0)',
        "The value of the field 'Labour Time' must be positive or 0.")]


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.depends('labour_line_ids.labour_time', 'labour_line_ids.labour_cost_profile_id.hour_cost')
    def _compute_total_labour_cost(self):
        for bom in self:
            cost = 0.0
            for lline in bom.labour_line_ids:
                cost += lline.labour_time * lline.labour_cost_profile_id.hour_cost
            bom.total_labour_cost = cost

    @api.depends('bom_line_ids.product_id.standard_price', 'total_labour_cost', 'extra_cost')
    def _compute_total_cost(self):
        for bom in self:
            component_cost = 0.0
            for line in bom.bom_line_ids:
                component_price = line.product_id.standard_price
                component_qty_product_uom = line.product_uom_id._compute_quantity(
                    line.product_qty, line.product_id.uom_id)
                component_cost += component_price * component_qty_product_uom
            total_cost = component_cost + bom.extra_cost + bom.total_labour_cost
            bom.total_components_cost = component_cost
            bom.total_cost = total_cost

    labour_line_ids = fields.One2many(
        'mrp.bom.labour.line', 'bom_id', string='Labour Lines')
    total_labour_cost = fields.Float(
        compute='_compute_total_labour_cost', readonly=True,
        digits=dp.get_precision('Product Price'),
        string="Total Labour Cost", store=True)
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
        compute='_compute_total_cost', readonly=True,
        string='Total Cost',
        digits=dp.get_precision('Product Price'),
        help="Total Cost = Total Components Cost + "
        "Total Labour Cost + Extra Cost")
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')
        # to display in bom lines

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    standard_price = fields.Float(
        related='product_id.standard_price', readonly=True,
        string='Standard Price')

    def manual_update_product_standard_price(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        if 'product_price_history_origin' not in ctx:
            ctx['product_price_history_origin'] = u'Manual update from BOM'
        precision = self.pool['decimal.precision'].precision_get(
            cr, uid, 'Product Price')
        for bom in self.browse(cr, uid, ids, context=context):
            if not bom.product_id:
                continue
            if float_compare(
                    bom.product_id.standard_price, bom.total_cost,
                    precision_digits=precision):
                bom.product_id.write(
                        {'standard_price': bom.total_cost}, context=ctx)
                logger.info(
                    'Cost price updated to %s on product %s',
                    bom.total_cost, bom.product_id.name_get()[0][1])
        return True

    def _phantom_update_product_standard_price(self, cr, uid, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        ctx['product_price_history_origin'] = 'Automatic update of Phantom BOMs'
        mbo = self.pool['mrp.bom']
        bom_ids = mbo.search(
            cr, uid, [('type', '=', 'phantom')], context=context)
        self.manual_update_product_standard_price(
            cr, uid, bom_ids, context=ctx)
        return True


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
        default=lambda self: self.env['res.company']._company_default_get())
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True, store=True,
        string='Company Currency')

    @api.depends('name', 'hour_cost', 'company_currency_id.symbol')
    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, u'%s (%s %s)' % (
                record.name, record.hour_cost,
                record.company_currency_id.symbol)))
        return res


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

    # TODO port to v12
    def compute_order_unit_cost(self, cr, uid, order, context=None):
        uuo = self.pool['uom.uom']
        mo_total_price = 0.0  # In the UoM of the M0
        labor_cost_per_unit = 0.0  # In the UoM of the product
        extra_cost_per_unit = 0.0  # In the UoM of the product
        # I read the raw materials MO, not on BOM, in order to make
        # it work with the "dynamic" BOMs (few raw material are auto-added
        # on the fly on MO)
        for raw_smove in order.move_lines + order.move_lines2:
            # I don't filter on state, in order to make it work with
            # partial productions
            # For partial productions, mo.product_qty is not updated
            # so we compute with fully qty and we compute with all raw
            # materials (consumed or not), so it gives a good price
            # per unit at the end
            raw_price = raw_smove.product_id.standard_price
            raw_qty_product_uom = uuo._compute_qty_obj(
                cr, uid, raw_smove.product_uom, raw_smove.product_qty,
                raw_smove.product_id.uom_id, context=context)
            raw_material_cost = raw_price * raw_qty_product_uom
            logger.info(
                'MO %s product %s: raw_material_cost=%s',
                order.name, raw_smove.product_id.name, raw_material_cost)
            mo_total_price += raw_material_cost
        if order.bom_id:
            bom = order.bom_id
            #if not bom.total_labour_cost:
            #    raise orm.except_orm(
            #        _('Error:'),
            #        _("Total Labor Cost is 0 on bill of material '%s'.")
            #        % bom.name)
            if not bom.product_qty:
                raise orm.except_orm(
                    _('Error:'),
                    _("Missing Product Quantity on bill of material '%s'.")
                    % bom.name)
            bom_qty_product_uom = uuo._compute_qty_obj(
                cr, uid, bom.product_uom, bom.product_qty,
                bom.product_id.uom_id, context=context)
            assert bom_qty_product_uom > 0, 'BoM qty should be positive'
            labor_cost_per_unit = bom.total_labour_cost / bom_qty_product_uom
            extra_cost_per_unit = bom.extra_cost / bom_qty_product_uom
        # mo_standard_price and labor_cost_per_unit are
        # in the UoM of the product (not of the MO/BOM)
        mo_qty_product_uom = uuo._compute_qty_obj(
            cr, uid, order.product_uom, order.product_qty,
            order.product_id.uom_id, context=context)
        assert mo_qty_product_uom > 0, 'MO qty should be positive'
        mo_standard_price = mo_total_price / mo_qty_product_uom
        logger.info(
            'MO %s: labor_cost_per_unit=%s', order.name, labor_cost_per_unit)
        logger.info(
            'MO %s: extra_cost_per_unit=%s', order.name, extra_cost_per_unit)
        mo_standard_price += labor_cost_per_unit
        mo_standard_price += extra_cost_per_unit
        order.write({'unit_cost': mo_standard_price}, context=context)
        logger.info(
            'MO %s: unit_cost=%s', order.name, mo_standard_price)
        return mo_standard_price

    def update_standard_price(self, cr, uid, order, context=None):
        if context is None:
            context = {}
        uuo = self.pool['uom.uom']
        product = order.product_id
        mo_standard_price = self.compute_order_unit_cost(
            cr, uid, order, context=context)
        mo_qty_product_uom = uuo._compute_qty_obj(
            cr, uid, order.product_uom, order.product_qty,
            order.product_id.uom_id, context=context)
        # I can't use the native method _update_average_price of stock.move
        # because it only works on move.picking_id.type == 'in'
        # As we do the super() at the END of this method,
        # the qty produced by this MO in NOT counted inside
        # product.qty_available
        qty_before_mo = product.qty_available
        logger.info(
            'MO %s product %s: standard_price before production: %s',
            order.name, product.name, product.standard_price)
        logger.info(
            'MO %s product %s: qty before production: %s',
            order.name, product.name, qty_before_mo)
        # Here, we handle as if we were in v8 (!)
        # so we consider that standard_price is in company currency
        # It will not work if you are in multi-company environment
        # with companies in different currencies
        if not qty_before_mo + mo_qty_product_uom:
            new_std_price = mo_standard_price
        else:
            new_std_price = (
                (product.standard_price * qty_before_mo) +
                (mo_standard_price * mo_qty_product_uom)) / \
                (qty_before_mo + mo_qty_product_uom)
        ctx_product = context.copy()
        ctx_product['product_price_history_origin'] = _(
            '%s (Qty before: %s - Added qty: %s - Unit price of '
            'added qty: %s)') % (
            order.name, qty_before_mo, mo_qty_product_uom, mo_standard_price)
        product.write({'standard_price': new_std_price}, context=ctx_product)
        logger.info(
            'MO %s product %s: standard_price updated to %s',
            order.name, product.name, new_std_price)
        return True

    def action_produce(
            self, cr, uid, production_id, production_qty, production_mode,
            context=None):
        if production_mode == 'consume_produce':
            order = self.browse(cr, uid, production_id, context=context)
            if order.product_id.cost_method == 'average':
                self.update_standard_price(cr, uid, order, context=context)
        return super(MrpProduction, self).action_produce(
            cr, uid, production_id, production_qty, production_mode,
            context=context)
