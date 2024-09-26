# Copyright 2024 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    def _default_show_operations(self):
        # super is not called as we want to always force the value to False
        # super()._default_show_operations()
        return False

    show_operations = fields.Boolean(default=lambda s: s._default_show_operations())
