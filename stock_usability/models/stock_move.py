# Copyright 2014-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

#    def name_get(self):
#        '''name_get of stock_move is important for the reservation of the
#        quants: so want to add the name of the customer and the expected date
#        in it'''
#        res = []
#        for line in self:
#            name = '%s > %s' % (
#                line.location_id.name, line.location_dest_id.name)
#            if line.product_id.code:
#                name = '%s: %s' % (line.product_id.code, name)
#            if line.picking_id.origin:
#                name = '%s %s' % (line.picking_id.origin, name)
#            if line.partner_id:
#                name = '%s %s' % (line.partner_id.name, name)
#            if line.date_expected:
#                name = '%s %s' % (name, line.date_expected)
#            res.append((line.id, name))
#        return res

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

    # TODO: I think it's not complete
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
