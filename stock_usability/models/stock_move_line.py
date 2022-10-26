# Copyright 2014-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # for optional display in tree view
    product_barcode = fields.Char(
        related='product_id.barcode', string="Product Barcode")

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
                picking.message_post(body=_(
                    "Product <a href=# data-oe-model=product.product "
                    "data-oe-id=%d>%s</a> qty %s %s <b>unreserved</b>")
                    % (product.id, product.display_name,
                       moveline.reserved_qty, product.uom_id.name))
                # Copied from do_unreserved of stock.picking
                picking.package_level_ids.filtered(lambda p: not p.move_ids).unlink()
            moveline.unlink()
