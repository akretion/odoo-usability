# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    layout_category_id = fields.Many2one(
        'sale.layout_category', string='Layout Category', ondelete='restrict',
        help="Default section on quotations for this product. If this field "
        "is empty but the equivalent field on the related product category "
        "is set, it will use the layout category configured on the product "
        "category")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def get_layout_category(self):
        self.ensure_one()
        res = self.env['sale.layout_category']
        if self.layout_category_id:
            res = self.layout_category_id
        elif self.categ_id.layout_category_id:
            res = self.categ_id.layout_category_id
        return res


class ProductCategory(models.Model):
    _inherit = 'product.category'

    layout_category_id = fields.Many2one(
        'sale.layout_category', string='Layout Category',
        help="Default section on quotations for the products of this "
        "category.")


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'

    product_tmpl_ids = fields.One2many(
        'product.template', 'layout_category_id',
        string='Products')
    product_categ_ids = fields.One2many(
        'product.category', 'layout_category_id',
        string='Product Categories', domain=[('type', '!=', 'view')])


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def layout_product_id_change(self):
        if self.product_id:
            self.layout_category_id = self.product_id.get_layout_category()
        else:
            self.layout_category_id = False
