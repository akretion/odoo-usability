# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def _prepare_stock_move_vals(
            self, picking, price_unit, product_uom_qty, product_uom):
        vals = super()._prepare_stock_move_vals(
            picking, price_unit, product_uom_qty, product_uom)
        # native : product.description_pickingin or self.name
        vals['description_picking'] = self.name
        return vals
