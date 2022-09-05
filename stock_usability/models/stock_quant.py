# Copyright 2014-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_barcode = fields.Char(
        related='product_id.barcode', string="Product Barcode")

    def action_stock_move_lines_reserved(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_move_line_action")
        action['domain'] = [
            ('state', 'not in', ('draft', 'done')),
            ('product_id', '=', self.product_id.id),
            ('location_id', '=', self.location_id.id),
            ('lot_id', '=', self.lot_id.id or False),
            '|',
            ('package_id', '=', self.package_id.id or False),
            ('result_package_id', '=', self.package_id.id or False),
        ]
        action['context'] = {'create': 0}
        return action
