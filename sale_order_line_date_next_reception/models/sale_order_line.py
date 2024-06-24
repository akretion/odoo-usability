# Copyright 2024 Akretion (http://www.akretion.com).
# @author Mathieu DELVA <mathieu.delva@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    date_next_reception = fields.Date(compute="_compute_date_next_reception")

    def _compute_date_next_reception(self):
        for line in self:
            line.date_next_reception = False
            if not(line.product_id.qty_available):
                purchase_order_lines = line.product_id.purchase_order_line_ids
                line.date_next_reception = purchase_order_lines and purchase_order_lines[0].date_planned
