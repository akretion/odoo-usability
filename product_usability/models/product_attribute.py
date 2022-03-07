# Copyright (C) 2022 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    values_count = fields.Integer(compute="_compute_values_count")

    @api.depends("value_ids")
    def _compute_values_count(self):
        for attr in self:
            attr.values_count = len(attr.value_ids)

    def show_values_ids(self):
        return {
            "name": "Attributes Lines",
            "type": "ir.actions.act_window",
            "res_id": self.id,
            "view_mode": "tree",
            "res_model": "product.attribute.value",
            "view_id":self.env.ref("product_usability.product_attribute_value_view_tree").id,
            "target": "current",
            "domain": [("id", "in", self.value_ids.ids)],
        }
