# Copyright 2014-2024 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _product_supplied_count(self):
        for partner in self:
            count = 0
            sellers = self.env['product.supplierinfo'].search(
                [('name', '=', partner.id)])
            if sellers:
                count = self.env['product.template'].search_count(
                    [('seller_ids', 'in', sellers.ids)])
            partner.product_supplied_count = count

    product_supplied_count = fields.Integer(
        compute='_product_supplied_count', string="# of Products Supplied",
        )

    def show_supplied_products(self):
        self.ensure_one()
        sellers = self.env['product.supplierinfo'].search(
            [('name', '=', self.id)])
        ptemplates = self.env['product.template'].search(
            [('seller_ids', 'in', sellers.ids)])
        action = {
            'name': _('Products'),
            'type': "ir.actions.act_window",
            "res_model": "product.template",
            "view_mode": 'tree,kanban,form',
            'domain': f"[('id', 'in', {ptemplates.ids})]",
            }
        return action
