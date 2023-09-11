# Copyright 2014-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    product_barcode = fields.Char(
        related='product_id.barcode', string="Product Barcode")

    def action_stock_move_lines_reserved(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_move_line_action")
        action['domain'] = [
            ('state', 'not in', ('draft', 'done', 'cancel')),
            ('reserved_uom_qty', '!=', 0),
            ('product_id', '=', self.product_id.id),
            ('location_id', '=', self.location_id.id),
            ('lot_id', '=', self.lot_id.id or False),
            '|',
            ('package_id', '=', self.package_id.id or False),
            ('result_package_id', '=', self.package_id.id or False),
        ]
        action['context'] = {'create': 0}
        return action

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if (
                not res.get('location_id') and
                self._context.get('search_location') and
                isinstance(self._context['search_location'], list) and
                len(self._context['search_location']) == 1):
            res['location_id'] = self._context['search_location'][0]
        return res

    @api.model
    def action_view_inventory(self):
        action = super().action_view_inventory()
        # Remove filter 'My Counts' set by default for Stock Users
        if (
                action.get('context') and
                isinstance(action['context'], dict) and
                action['context'].get('search_default_my_count')):
            action['context'].pop('search_default_my_count')
        return action
