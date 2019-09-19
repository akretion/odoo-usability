# Copyright 2014-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
import logging

logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    _order = 'id desc'
    # In the stock module: _order = "priority desc, date asc, id desc"
    # The problem is date asc

    partner_id = fields.Many2one(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    move_type = fields.Selection(track_visibility='onchange')
    # Can be used in view to hide some fields depending of pick type
    picking_type_code = fields.Selection(related='picking_type_id.code')

    @api.multi
    def do_unreserve(self):
        res = super(StockPicking, self).do_unreserve()
        for pick in self:
            pick.message_post(body=_("Picking <b>unreserved</b>."))
        return res


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

    @api.multi
    def name_get(self):
        '''name_get of stock_move is important for the reservation of the
        quants: so want to add the name of the customer and the expected date
        in it'''
        res = []
        for line in self:
            name = '%s > %s' % (
                line.location_id.name, line.location_dest_id.name)
            if line.product_id.code:
                name = '%s: %s' % (line.product_id.code, name)
            if line.picking_id.origin:
                name = '%s %s' % (line.picking_id.origin, name)
            if line.partner_id:
                name = '%s %s' % (line.partner_id.name, name)
            if line.date_expected:
                name = '%s %s' % (name, line.date_expected)
            res.append((line.id, name))
        return res

    def button_do_unreserve(self):
        for move in self:
            move._do_unreserve()
            picking = move.picking_id
            if picking:
                product = move.product_id
                picking.message_post(_(
                    "Product <a href=# data-oe-model=product.product "
                    "data-oe-id=%d>%s</a> qty %s %s <b>unreserved</b>")
                    % (product.id, product.display_name,
                       move.product_qty, product.uom_id.name))
                # Copied from do_unreserved of stock.picking
                picking.package_level_ids.filtered(lambda p: not p.move_ids).unlink()


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def button_do_unreserve(self):
        for moveline in self:
            if moveline.state == 'cancel':
                continue
            elif moveline.state == 'done':
                raise UserError(_(
                    "You cannot unreserve a move line in done state."))
            picking = moveline.move_id.picking_id
            if picking:
                product = moveline.product_id
                picking.message_post(_(
                    "Product <a href=# data-oe-model=product.product "
                    "data-oe-id=%d>%s</a> qty %s %s <b>unreserved</b>")
                    % (product.id, product.display_name,
                       moveline.product_qty, product.uom_id.name))
                # Copied from do_unreserved of stock.picking
                picking.package_level_ids.filtered(lambda p: not p.move_ids).unlink()
            moveline.unlink()


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    picking_ids = fields.One2many(
        'stock.picking', 'group_id', string='Pickings', readonly=True)


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_stock_move_lines_reserved(self):
        self.ensure_one()
        action = self.action_view_stock_moves()
        action['context'] = {'search_default_todo': True}
        return action
