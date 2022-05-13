# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_open_stock_valuation_layer(self):
        self.ensure_one()
        ppo = self.env['product.product']
        if len(self.product_variant_ids) == 1:
            action = ppo._get_stock_valuation_layer_action(self.product_variant_ids.id)
        else:
            action = ppo._get_stock_valuation_layer_action()
            action["domain"] = [('product_id', 'in', self.product_variant_ids.ids)]
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_open_stock_valuation_layer(self):
        self.ensure_one()
        return self._get_stock_valuation_layer_action(self.id)

    @api.model
    def _get_stock_valuation_layer_action(self, product_id=None):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock_account.stock_valuation_layer_action")
        if product_id:
            action["context"] = {
                'search_default_product_id': product_id,
                'search_default_group_by_product_id': 1,
                }
        return action
