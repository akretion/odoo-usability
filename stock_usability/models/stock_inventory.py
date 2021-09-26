# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    prefill_counted_quantity = fields.Selection(
        readonly=True, states={'draft': [('readonly', False)]})


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    product_barcode = fields.Char(related='product_id.barcode', string="Product Barcode")
    difference_qty = fields.Float(search="_search_difference_qty_usability")

    def _search_difference_qty_usability(self, operator, value):
        # Inspired by the method _search_difference_qty() from the
        # official stock module
        # So a part of this code is copyright Odoo SA under LGPL licence
        if not self.env.context.get('default_inventory_id'):
            raise NotImplementedError(_('Unsupported search on %s outside of an Inventory Adjustment', 'difference_qty'))
        lines = self.search([('inventory_id', '=', self.env.context.get('default_inventory_id'))])
        line_ids = []
        for line in lines:
            if operator == '=':
                if float_is_zero(line.difference_qty, line.product_id.uom_id.rounding):
                    line_ids.append(line.id)
            elif operator == '!=':
                if not float_is_zero(line.difference_qty, line.product_id.uom_id.rounding):
                    line_ids.append(line.id)
            elif operator == '>':
                if float_compare(line.difference_qty, 0, line.product_id.uom_id.rounding) > 0:
                    line_ids.append(line.id)
            elif operator == '<':
                if float_compare(line.difference_qty, 0, line.product_id.uom_id.rounding) < 0:
                    line_ids.append(line.id)
            else:
                raise NotImplementedError()
        return [('id', 'in', line_ids)]
