# -*- coding: utf-8 -*-
##############################################################################
#
#    MRP Average Cost module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import logging

logger = logging.getLogger(__name__)


class MrpBom(orm.Model):
    _inherit = 'mrp.bom'

    _columns = {
        'labour_time': fields.float(
            'Labour Time',
            digits_compute=dp.get_precision('Labour Hours'),
            help="Average labour time for the production of the quantity of "
            "items of the BOM, in hours."),
        'labour_cost_profile_id': fields.many2one(
            'labour.cost.profile', 'Labour Cost Profile')
        }


class LabourCostProfile(orm.Model):
    _name = 'labour.cost.profile'
    _inherit = ['mail.thread']
    _description = 'Labour Cost Profile'

    _columns = {
        'name': fields.char(
            'Name', required=True, track_visibility='onchange'),
        'hour_cost': fields.float(
            'Cost per Hour', required=True,
            digits_compute=dp.get_precision('Product Price'),
            track_visibility='onchange',
            help="Labour cost per hour per person in company currency"),
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'company_currency_id': fields.related(
            'company_id', 'currency_id', readonly=True, type='many2one',
            relation='res.currency', string='Company Currency')
        }

    _defaults = {
        'company_id': lambda self, cr, uid, context:
        self.pool['res.company']._company_default_get(
            cr, uid, 'labour.cost.profile', context=context),
        }

    def name_get(self, cr, uid, ids, context=None):
        res = []
        if isinstance(ids, (int, long)):
            ids = [ids]
        for record in self.browse(cr, uid, ids, context=context):
            res.append((record.id, u'%s (%s %s)' % (
                record.name, record.hour_cost,
                record.company_currency_id.symbol)))
        return res


class MrpProduction(orm.Model):
    _inherit = 'mrp.production'

    _columns = {
        'unit_cost': fields.float(
            'Unit Cost', readonly=True,
            digits_compute=dp.get_precision('Product Price'),
            help="This cost per unit in the unit of measure of the product "
            "in company currency takes into account "
            "the cost of the raw materials and the labour cost defined on"
            "the BOM."),
        'company_currency_id': fields.related(
            'company_id', 'currency_id', readonly=True, type='many2one',
            relation='res.currency', string='Company Currency'),
        }

    def update_standard_price(self, cr, uid, order, context=None):
        if context is None:
            context = {}
        puo = self.pool['product.uom']
        mo_total_price = 0.0  # In the UoM of the M0
        labor_cost_per_unit = 0.0  # In the UoM of the product
        product = order.product_id
        # I read the raw materials MO, not on BOM, in order to make
        # it work with the "dynamic" BOMs (few raw material are auto-added
        # on the fly on MO)
        for raw_smove in order.move_lines:
            # I don't filter on state, in order to make it work with
            # partial productions
            # For partial productions, mo.product_qty is not updated
            # so we compute with fully qty and we compute with all raw
            # materials (consumed or not), so it gives a good price
            # per unit at the end
            raw_price = raw_smove.product_id.standard_price
            raw_qty_product_uom = puo._compute_qty_obj(
                cr, uid, raw_smove.product_uom, raw_smove.product_qty,
                raw_smove.product_id.uom_id, context=context)
            raw_material_cost = raw_price * raw_qty_product_uom
            logger.info(
                'MO %s product %s: raw_material_cost=%s',
                order.name, raw_smove.product_id.name, raw_material_cost)
            mo_total_price += raw_material_cost
        if order.bom_id:
            bom = order.bom_id
            if not bom.labour_cost_profile_id:
                raise orm.except_orm(
                    _('Error:'),
                    _("Labor Cost Profile is not set on bill of "
                        "material '%s'.") % bom.name)
            if not bom.labour_time:
                raise orm.except_orm(
                    _('Error:'),
                    _("Labour Time is not set on bill of material '%s'.")
                    % bom.name)
            if not bom.product_qty:
                raise orm.except_orm(
                    _('Error:'),
                    _("Missing Product Quantity on bill of material '%s'.")
                    % bom.name)
            bom_qty_product_uom = puo._compute_qty_obj(
                cr, uid, bom.product_uom, bom.product_qty,
                bom.product_id.uom_id, context=context)
            assert bom_qty_product_uom > 0, 'BoM qty should be positive'
            labor_cost_per_unit = (
                bom.labour_time * bom.labour_cost_profile_id.hour_cost) /\
                bom_qty_product_uom
        # mo_standard_price and labor_cost_per_unit are
        # in the UoM of the product (not of the MO/BOM)
        mo_qty_product_uom = puo._compute_qty_obj(
            cr, uid, order.product_uom, order.product_qty,
            order.product_id.uom_id, context=context)
        assert mo_qty_product_uom > 0, 'MO qty should be positive'
        mo_standard_price = mo_total_price / mo_qty_product_uom
        logger.info(
            'MO %s: labor_cost_per_unit=%s', order.name, labor_cost_per_unit)
        mo_standard_price += labor_cost_per_unit
        order.write({'unit_cost': mo_standard_price}, context=context)
        logger.info(
            'MO %s: mo_standard_price=%s', order.name, mo_standard_price)
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
