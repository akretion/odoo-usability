# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductCategTaxMixin(models.AbstractModel):
    _name = 'product.categ.tax.mixin'

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        if self.categ_id:
            self.taxes_id, self.supplier_taxes_id = (
                self.apply_tax_from_category(self.categ_id))

    @api.model
    def apply_tax_from_category(self, categ):
        # I cannot use the commented line below:
        # self.taxes_id = self.categ_id.sale_tax_ids.ids
        #   because it ADDS the taxes (equivalent of (4, ID)) instead
        #   of replacing the taxes... and I want to REPLACE the taxes
        #   So I have to use the awful syntax (6, 0, [IDs])
        # values are sent to ('taxes_id' and 'supplier_taxes_id')
        return ([(6, 0, categ.sale_tax_ids.ids)],
                [(6, 0, categ.purchase_tax_ids.ids)])

    @api.model
    def write_or_create(self, vals):
        if vals.get('categ_id'):
            categ = self.env['product.category'].browse(vals['categ_id'])
            vals['taxes_id'], vals['supplier_taxes_id'] =\
                self.apply_tax_from_category(categ)

    @api.model
    def create(self, vals):
        self.write_or_create(vals)
        return super(ProductCategTaxMixin, self).create(vals)

    @api.multi
    def write(self, vals):
        self.write_or_create(vals)
        return super(ProductCategTaxMixin, self).write(vals)


class ProductTemplate(models.Model):
    _inherit = ['product.template', 'product.categ.tax.mixin']
    _name = 'product.template'

    @api.one
    @api.constrains('taxes_id', 'supplier_taxes_id')
    def _check_tax_categ(self):
        # self.name != 'Pay Debt' is a stupid hack to avoid blocking the
        # installation of the module 'pos_debt_notebook'
        if self.categ_id:   # and self.name != 'Pay Debt':
            if self.categ_id.sale_tax_ids.ids != self.taxes_id.ids:
                raise ValidationError(_(
                    "The sale taxes configured on the product '%s' "
                    "are not the same as the sale taxes configured "
                    "on it's related internal category '%s'.")
                    % (self.name, self.categ_id.name_get()[0][1]))
            if (
                    self.categ_id.purchase_tax_ids.ids !=
                    self.supplier_taxes_id.ids):
                raise ValidationError(_(
                    "The purchase taxes configured on the product '%s' "
                    "are not the same as the purchase taxes configured "
                    "on it's related internal category '%s'.")
                    % (self.name, self.categ_id.name_get()[0][1]))


class ProductProduct(models.Model):
    _inherit = ['product.product', 'product.categ.tax.mixin']
    _name = 'product.product'


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sale_tax_ids = fields.Many2many(
        'account.tax', 'product_categ_sale_tax_rel', 'categ_id', 'tax_id',
        string="Sale Taxes", domain=[('type_tax_use', '=', 'sale')])
    purchase_tax_ids = fields.Many2many(
        'account.tax', 'product_categ_purchase_tax_rel', 'categ_id', 'tax_id',
        string="Purchase Taxes", domain=[('type_tax_use', '=', 'purchase')])
