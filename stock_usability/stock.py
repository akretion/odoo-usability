# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Usability module for Odoo
#    Copyright (C) 2014-2016 Akretion (http://www.akretion.com)
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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
import logging

logger = logging.getLogger(__name__)


class StockInventory(models.Model):
    _inherit = 'stock.inventory'
    _order = 'id desc'


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'id desc'
    # In the stock module: _order = "priority desc, date asc, id desc"
    # The problem is date asc

    partner_id = fields.Many2one(track_visibility='onchange')

    @api.multi
    def force_assign(self):
        res = super(StockPicking, self).force_assign()
        for pick in self:
            pick.message_post(_("Using <b>Force Availability</b>!"))
        return res


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


class StockMove(models.Model):
    _inherit = 'stock.move'

    def name_get(self, cr, uid, ids, context=None):
        '''name_get of stock_move is important for the reservation of the
        quants: so want to add the name of the customer and the expected date
        in it'''
        res = []
        for line in self.browse(cr, uid, ids, context=context):
            name = line.location_id.name + ' > ' + line.location_dest_id.name
            if line.product_id.code:
                name = line.product_id.code + ': ' + name
            if line.picking_id.origin:
                name = line.picking_id.origin + ' ' + name
            if line.partner_id:
                name = line.partner_id.name + ' ' + name
            if line.date_expected:
                date_expec_dt = fields.Datetime.from_string(line.date_expected)
                name = name + ' ' + fields.Date.to_string(date_expec_dt)
            res.append((line.id, name))
        return res


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    uom_id = fields.Many2one(
        'product.uom', related='product_id.uom_id', readonly=True)


class StockIncoterms(models.Model):
    _inherit = 'stock.incoterms'

    @api.multi
    def name_get(self):
        res = []
        for inco in self:
            res.append((inco.id, u'[%s] %s' % (inco.code, inco.name)))
        return res
