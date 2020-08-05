# Copyright (C) 2020 - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_view_bom(self):
        """Replace native action `template_open_bom` to distinguish if we will display
        only one BoM form or a list of BoMs."""
        self.ensure_one()

        act_window_xml_id = "mrp.mrp_bom_form_action"
        act_window = self.env.ref(act_window_xml_id).read()[0]
        if self.bom_count > 1:
            act_window["context"] = {
                "default_product_tmpl_id": self.id,
                "search_default_product_tmpl_id": self.id,
            }
        else:
            act_window["context"] = {"default_product_tmpl_id": self.id}
            act_window["views"] = [(self.env.ref("mrp.mrp_bom_form_view").id, "form")]
            act_window["res_id"] = (
                self.env["mrp.bom"].search([("product_tmpl_id", "=", self.id)]).id
            )

        return act_window


class ProductProduct(models.Model):
    _inherit = "product.product"

    def action_view_bom(self):
        res = super().action_view_bom()

        bom_target_ids = self.env["mrp.bom"].search(res["domain"])

        if len(bom_target_ids) == 1:
            res["views"] = [(self.env.ref("mrp.mrp_bom_form_view").id, "form")]
            res["res_id"] = bom_target_ids[0].id

        return res
