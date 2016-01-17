# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Usability module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
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

from openerp import models, fields
import openerp.addons.decimal_precision as dp
import logging

logger = logging.getLogger(__name__)


class StockInventory(models.Model):
    _inherit = 'stock.inventory'
    _order = 'id desc'


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'id desc'


class StockLocation(models.Model):
    _inherit = 'stock.location'

    name = fields.Char(translate=False)
    # with the 'quant_ids' field below, you can for example search empty stock
    # locations with self.env['stock.location'].search([
    #    ('child_ids', '=', False), ('quant_ids', '=', False),
    #    ('usage', '=', 'internal')])
    quant_ids = fields.One2many(
        'stock.quant', 'location_id', string="Related Quants")


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    name = fields.Char(translate=False)


class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    name = fields.Char(translate=False)


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    _sql_constraints = [(
        'company_wh_location_product_unique',
        'unique(company_id, warehouse_id, location_id, product_id)',
        'An orderpoint already exists for the same company, same warehouse, '
        'same stock location and same product.'
        )]


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    qty = fields.Float(digits=dp.get_precision('Product Unit of Measure'))


class StockMove(models.Model):
    _inherit = 'stock.move'

    reserved_availability = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'))
    availability = fields.Float(
        digits=dp.get_precision('Product Unit of Measure'))


class StockMoveOperationLink(models.Model):
    _inherit = 'stock.move.operation.link'

    qty = fields.Float(digits=dp.get_precision('Product Unit of Measure'))


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"

    def _procure_orderpoint_confirm(
            self, cr, uid, use_new_cursor=False, company_id=False,
            context=None):
        logger.info(
            'procurement scheduler: START to create procurements from '
            'orderpoints')
        res = super(ProcurementOrder, self)._procure_orderpoint_confirm(
            cr, uid, use_new_cursor=use_new_cursor, company_id=company_id,
            context=context)
        logger.info(
            'procurement scheduler: END creation of procurements from '
            'orderpoints')
        return res
