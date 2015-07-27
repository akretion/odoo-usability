# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Margin module for Odoo
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

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    standard_price_company_currency = fields.Float(
        string='Cost Price in Company Currency', readonly=True,
        digits=dp.get_precision('Product Price'))
    standard_price_invoice_currency = fields.Float(
        string='Cost Price in Invoice Currency', readonly=True,
        compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))
    margin_invoice_currency = fields.Float(
        string='Margin in Invoice Currency', readonly=True, store=True,
        compute='_compute_margin',
        digits=dp.get_precision('Account'))
    margin_company_currency = fields.Float(
        string='Margin in Company Currency', readonly=True, store=True,
        compute='_compute_margin',
        digits=dp.get_precision('Account'))

    @api.one
    @api.depends(
        'standard_price_company_currency', 'invoice_id.currency_id',
        'invoice_id.move_id',
        'invoice_id.date_invoice', 'quantity', 'price_subtotal')
    def _compute_margin(self):
        standard_price_inv_cur = 0.0
        margin_inv_cur = 0.0
        margin_comp_cur = 0.0
        if self.invoice_id:
            # it works in _get_current_rate
            # even if we set date = False in context
            standard_price_inv_cur =\
                self.invoice_id.company_id.currency_id.with_context(
                    date=self.invoice_id.date_invoice).compute(
                        self.standard_price_company_currency,
                        self.invoice_id.currency_id)
            margin_inv_cur =\
                self.price_subtotal - self.quantity * standard_price_inv_cur
            margin_comp_cur = self.invoice_id.currency_id.with_context(
                date=self.invoice_id.date_invoice).compute(
                    margin_inv_cur, self.invoice_id.company_id.currency_id)
        self.standard_price_invoice_currency = standard_price_inv_cur
        self.margin_invoice_currency = margin_inv_cur
        self.margin_company_currency = margin_comp_cur

    # We want to copy standard_price on invoice line for customer
    # invoice/refunds. We can't do that via on_change of product_id,
    # because it is not always played when invoice is created from code
    # => we inherit write/create
    # We write standard_price_company_currency even on supplier invoice/refunds
    # because we don't have access to the 'type' of the invoice
    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            pp = self.env['product.product'].browse(vals['product_id'])
            vals['standard_price_company_currency'] = pp.standard_price
        return super(AccountInvoiceLine, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('product_id'):
            pp = self.env['product.product'].browse(vals['product_id'])
            vals['standard_price_company_currency'] = pp.standard_price
        return super(AccountInvoiceLine, self).write(vals)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    margin_invoice_currency = fields.Float(
        string='Margin in Invoice Currency',
        readonly=True, compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))
    margin_company_currency = fields.Float(
        string='Margin in Company Currency',
        readonly=True, compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))

    @api.one
    @api.depends(
        'currency_id', 'date_invoice', 'type', 'move_id',
        'invoice_line.margin_invoice_currency',
        'invoice_line.margin_company_currency')
    # I invalidate on move_id because the currency rate used for accounting
    # entries is the currency rate available on invoice validation, so when
    # the move_id field is written
    def _compute_margin(self):
        margin_inv_cur = 0.0
        margin_comp_cur = 0.0
        if self.type in ('out_invoice', 'out_refund'):
            for il in self.invoice_line:
                margin_inv_cur += il.margin_invoice_currency
                margin_comp_cur += il.margin_company_currency
        if self.type == 'out_refund':
            margin_inv_cur *= -1
            margin_comp_cur *= -1
        self.margin_invoice_currency = margin_inv_cur
        self.margin_company_currency = margin_comp_cur
