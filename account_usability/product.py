# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # DON'T put store=True on those fields, because they are company dependent
    sale_price_type = fields.Selection(
        '_sale_purchase_price_type_sel', compute='_compute_sale_price_type',
        string='Sale Price Type', compute_sudo=False, readonly=True)
    purchase_price_type = fields.Selection(
        '_sale_purchase_price_type_sel', compute='_compute_purchase_price_type',
        string='Purchase Price Type', compute_sudo=False, readonly=True)

    @api.model
    def _sale_purchase_price_type_sel(self):
        return [('incl', _('Tax incl.')), ('excl', _('Tax excl.'))]

    @api.depends('taxes_id')
    def _compute_sale_price_type(self):
        for pt in self:
            sale_price_type = 'incl'
            if pt.taxes_id and all([not t.price_include for t in pt.taxes_id if t.amount_type == 'percent']):
                sale_price_type = 'excl'
            pt.sale_price_type = sale_price_type

    @api.depends('supplier_taxes_id')
    def _compute_purchase_price_type(self):
        for pt in self:
            purchase_price_type = 'incl'
            if pt.supplier_taxes_id and all([not t.price_include for t in pt.supplier_taxes_id if t.amount_type == 'percent']):
                purchase_price_type = 'excl'
            pt.purchase_price_type = purchase_price_type


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    # DON'T put store=True on those fields, because they are company dependent
    purchase_price_type = fields.Selection(
        related='product_tmpl_id.purchase_price_type', related_sudo=False)
