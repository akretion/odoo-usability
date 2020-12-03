# Copyright (C) 2020 - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_view_bom(self):
        """Replace native action `template_open_bom` to distinguish if we will display
        only one BoM form or a list of BoMs."""
        self.ensure_one()
        if self.bom_count == 1:
            action = self.env.ref("mrp.mrp_bom_form_action").read()[0]
            bom = self.env["mrp.bom"].search([("product_tmpl_id", "=", self.id)])
            action.update({
                "context": {"default_product_tmpl_id": self.id},
                "views": False,
                "view_mode": "form,tree",
                "res_id": bom.id,
                })
        else:
            action = self.env.ref("mrp.template_open_bom").read()[0]
        return action


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_bom(self):
        action = super().action_view_bom()
        bom_target_ids = self.env["mrp.bom"].search(action["domain"])
        if len(bom_target_ids) == 1:
            action.update({
                "views": False,
                "view_mode": "form,tree",
                "res_id": bom_target_ids[0].id,
                })
        return action
