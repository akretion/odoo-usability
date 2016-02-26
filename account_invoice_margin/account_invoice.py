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
        digits=dp.get_precision('Product Price'),
        help="Cost price in company currency in the unit of measure "
        "of the invoice line (which may be different from the unit "
        "of measure of the product).")
    standard_price_invoice_currency = fields.Float(
        string='Cost Price in Invoice Currency', readonly=True,
        compute='_compute_margin', store=True,
        digits=dp.get_precision('Product Price'),
        help="Cost price in invoice currency in the unit of measure "
        "of the invoice line")
    margin_invoice_currency = fields.Float(
        string='Margin in Invoice Currency', readonly=True, store=True,
        compute='_compute_margin',
        digits=dp.get_precision('Account'))
    margin_company_currency = fields.Float(
        string='Margin in Company Currency', readonly=True, store=True,
        compute='_compute_margin',
        digits=dp.get_precision('Account'))
    margin_rate = fields.Float(
        string="Margin Rate", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.one
    @api.depends(
        'standard_price_company_currency', 'invoice_id.currency_id',
        'invoice_id.type', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'quantity', 'price_subtotal')
    def _compute_margin(self):
        standard_price_inv_cur = 0.0
        margin_inv_cur = 0.0
        margin_comp_cur = 0.0
        margin_rate = 0.0
        if (
                self.invoice_id and
                self.invoice_id.type in ('out_invoice', 'out_refund')):
            # it works in _get_current_rate
            # even if we set date = False in context
            # standard_price_inv_cur is in the UoM of the invoice line
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
            if self.price_subtotal:
                margin_rate = 100 * margin_inv_cur / self.price_subtotal
            # for a refund, margin should be negative
            # but margin rate should stay positive
            if self.invoice_id.type == 'out_refund':
                margin_inv_cur *= -1
                margin_comp_cur *= -1
        self.standard_price_invoice_currency = standard_price_inv_cur
        self.margin_invoice_currency = margin_inv_cur
        self.margin_company_currency = margin_comp_cur
        self.margin_rate = margin_rate

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
            std_price = pp.standard_price
            inv_uom_id = vals.get('uos_id')
            if inv_uom_id and inv_uom_id != pp.uom_id.id:
                std_price = self.env['product.uom']._compute_price(
                    pp.uom_id.id, std_price, inv_uom_id)
            vals['standard_price_company_currency'] = std_price
        return super(AccountInvoiceLine, self).create(vals)

    @api.multi
    def write(self, vals):
        if not vals:
            vals = {}
        if 'product_id' in vals or 'uos_id' in vals:
            for il in self:
                if 'product_id' in vals:
                    if vals.get('product_id'):
                        pp = self.env['product.product'].browse(
                            vals['product_id'])
                    else:
                        pp = False
                else:
                    pp = il.product_id or False
                # uos_id is NOT a required field
                if 'uos_id' in vals:
                    if vals.get('uos_id'):
                        inv_uom = self.env['product.uom'].browse(
                            vals['uos_id'])
                    else:
                        inv_uom = False
                else:
                    inv_uom = il.uos_id or False
                std_price = 0.0
                if pp:
                    std_price = pp.standard_price
                    if inv_uom and inv_uom != pp.uom_id:
                        std_price = self.env['product.uom']._compute_price(
                            pp.uom_id.id, std_price, inv_uom.id)
                il.write({'standard_price_company_currency': std_price})
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
        'type',
        'invoice_line.margin_invoice_currency',
        'invoice_line.margin_company_currency')
    def _compute_margin(self):
        margin_inv_cur = 0.0
        margin_comp_cur = 0.0
        if self.type in ('out_invoice', 'out_refund'):
            for il in self.invoice_line:
                margin_inv_cur += il.margin_invoice_currency
                margin_comp_cur += il.margin_company_currency
        self.margin_invoice_currency = margin_inv_cur
        self.margin_company_currency = margin_comp_cur
