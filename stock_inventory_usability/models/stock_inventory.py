# Copyright 2022 Akretion (https://www.akretion.com).
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models, api
from odoo.exceptions import UserError


class Inventory(models.Model):
    _inherit = "stock.inventory"

    prefill_counted_quantity = fields.Selection(default="zero")
    estimated_inventory_lines = fields.Float(compute="_compute_estimated_inventory_lines") #store ?

    @api.depends("location_ids", "product_ids")
    def _compute_estimated_inventory_lines(self):
        for inv in self:
            inv.estimated_inventory_lines = len(inv._get_quantities())
