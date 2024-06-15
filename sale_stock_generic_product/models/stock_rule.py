# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(
            self, product_id, product_qty, product_uom, location_dest_id, name,
            origin, company_id, values):
        move_vals = super()._get_stock_move_values(
            product_id, product_qty, product_uom, location_dest_id, name,
            origin, company_id, values)
        move_vals['description_picking'] = values.get('description_picking')
        return move_vals
