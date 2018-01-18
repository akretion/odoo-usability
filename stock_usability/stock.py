# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
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
    picking_type_id = fields.Many2one(track_visibility='onchange')
    move_type = fields.Selection(track_visibility='onchange')

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

    # This is for the button shortcut "reordering rules" on
    # stock.location form view, so that the location_id has the
    # good value, not the default stock location of the first WH of the company
    @api.model
    def default_get(self, fields):
        if self._context.get('default_location_id'):
            location = self.env['stock.location'].browse(
                self._context['default_location_id'])
            wh = location.get_warehouse()
            if location and wh:
                self = self.with_context(default_warehouse_id=wh.id)
        return super(StockWarehouseOrderpoint, self).default_get(fields)

    # This SQL constraint blocks the use of the "active" field
    # but I think it's not very useful to have such an "active" field
    # on orderpoints ; when you think the order point is bad, you update
    # the min/max values, you don't de-active it !
    _sql_constraints = [(
        'company_wh_location_product_unique',
        'unique(company_id, warehouse_id, location_id, product_id)',
        'An orderpoint already exists for the same company, same warehouse, '
        'same stock location and same product.'
        )]


class StockMove(models.Model):
    _inherit = 'stock.move'

# It seems that it is not necessary any more to
# have the digits= on these 2 fields to fix the bug
# https://github.com/odoo/odoo/pull/10038
#    reserved_availability = fields.Float(
#        digits=dp.get_precision('Product Unit of Measure'))
#    availability = fields.Float(
#        digits=dp.get_precision('Product Unit of Measure'))

    @api.multi
    def name_get(self):
        '''name_get of stock_move is important for the reservation of the
        quants: so want to add the name of the customer and the expected date
        in it'''
        res = []
        for line in self:
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


class StockIncoterms(models.Model):
    _inherit = 'stock.incoterms'

    @api.multi
    def name_get(self):
        res = []
        for inco in self:
            res.append((inco.id, u'[%s] %s' % (inco.code, inco.name)))
        return res


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    picking_ids = fields.One2many(
        'stock.picking', 'group_id', string='Pickings', readonly=True)
