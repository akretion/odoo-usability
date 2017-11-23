# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    name = fields.Char(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    categ_id = fields.Many2one(track_visibility='onchange')
    list_price = fields.Float(track_visibility='onchange')
    sale_ok = fields.Boolean(track_visibility='onchange')
    purchase_ok = fields.Boolean(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')

    def show_product_price_history(self):
        self.ensure_one()
        products = self.env['product.product'].search(
            [('product_tmpl_id', '=', self._context['active_id'])])
        action = self.env['ir.actions.act_window'].for_xml_id(
            'product_usability', 'product_price_history_action')
        action.update({
            'domain': "[('id', 'in', %s)]" % products.ids,
        })
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(track_visibility='onchange', copy=False)
    barcode = fields.Char(track_visibility='onchange')
    weight = fields.Float(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    price_history_ids = fields.One2many(
        'product.price.history', 'product_id',
        string='Product Price History')

    _sql_constraints = [(
        # Maybe it could be better to have a constrain per company
        # but the company_id field is on product.template,
        # not on product.product
        # If it's a problem, we'll create a company_id field on
        # product.product
        'default_code_uniq',
        'unique(default_code)',
        'This internal reference already exists!')]

    def show_product_price_history(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'product_usability', 'product_price_history_action')
        action.update({
            'domain': "[('product_id', '=', %d)]" % self.ids[0],
        })
        return action


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    name = fields.Many2one(
        domain=[('supplier', '=', True), ('parent_id', '=', False)])


class ProductPriceHistory(models.Model):
    _inherit = 'product.price.history'

    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True,
        string='Company Currency')
