# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
import pprint


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    def _get_location_fields(self):
        location_fields = []

        for field, definition in self.fields_get().items():
            if definition.get("relation") == "stock.location":
                location_fields.append(field)

        return location_fields

    def _check_locations_created_by_warehouse(self):
        location_ids = self.env["stock.location"]
        location_fields = self._get_location_fields()

        for rec in self:
            for field in location_fields:
                location_ids |= getattr(rec, field)

        location_ids.write({"is_created_by_warehouse": True})

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res._check_locations_created_by_warehouse()
        return res
