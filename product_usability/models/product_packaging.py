# Copyright Akretion (http://www.akretion.com/)

from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    def ui_goto_packaging_view(self):
        self.ensure_one()
        action = self.env.ref("product.action_packaging_view")._get_action_dict()
        action["context"] = {
            "search_default_product_id": self.product_id.id,
        }
        action[
            "domain"
        ] = f"[('product_id', 'in', {self.product_id.product_tmpl_id.product_variant_ids.ids})]"
        return action
