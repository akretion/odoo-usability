# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Category Tax module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ProductCategTaxMixin(models.AbstractModel):
    _name = 'product.categ.tax.mixin'

    @api.onchange('categ_id')
    def onchange_categ_id(self):
        if self.categ_id:
            self.taxes_id, self.supplier_taxes_id = (
                self.apply_tax_from_category(self.categ_id))

    @api.model
    def apply_tax_from_category(self, categ_id):
        # self.ensure_one()
        #   I cannot use the commented line below:
        # self.taxes_id = self.categ_id.sale_tax_ids.ids
        #   because it ADDS the taxes (equivalent of (4, ID)) instead
        #   of replacing the taxes... and I want to REPLACE the taxes
        #   So I have to use the awful syntax (6, 0, [IDs])
        # values are sent to ('taxes_id' and 'supplier_taxes_id')
        return ([(6, 0, categ_id.sale_tax_ids.ids)],
                [(6, 0, categ_id.purchase_tax_ids.ids)])

    @api.model
    def write_or_create(self, vals):
        if vals.get('categ_id'):
            vals['taxes_id'], vals['supplier_taxes_id'] = (
                self.apply_tax_from_category(
                    self.categ_id.browse(vals['categ_id'])))

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
        if self.categ_id and self.name != 'Pay Debt':
            if self.categ_id.sale_tax_ids.ids != self.taxes_id.ids:
                raise ValidationError(
                    _("The sale taxes configured on the product '%s' "
                        "are not the same as the sale taxes configured "
                        "on it's related product category '%s'.")
                    % (self.name, self.categ_id.complete_name))
            if (
                    self.categ_id.purchase_tax_ids.ids !=
                    self.supplier_taxes_id.ids):
                raise ValidationError(
                    _("The purchase taxes configured on the product '%s' "
                        "are not the same as the purchase taxes configured "
                        "on it's related product category '%s'.")
                    % (self.name, self.categ_id.complete_name))


class ProductProduct(models.Model):
    _inherit = ['product.product', 'product.categ.tax.mixin']
    _name = 'product.product'


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sale_tax_ids = fields.Many2many(
        'account.tax', 'product_categ_sale_tax_rel', 'categ_id', 'tax_id',
        string="Sale Taxes",
        domain=[
            ('parent_id', '=', False),
            ('type_tax_use', 'in', ['sale', 'all'])])
    purchase_tax_ids = fields.Many2many(
        'account.tax', 'product_categ_purchase_tax_rel', 'categ_id', 'tax_id',
        string="Purchase Taxes",
        domain=[
            ('parent_id', '=', False),
            ('type_tax_use', 'in', ['purchase', 'all'])])
