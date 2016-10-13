# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Invoice Margin module for Odoo
#    Copyright (C) 2015-2016 Akretion (http://www.akretion.com)
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

from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(orm.Model):
    _inherit = 'account.invoice.line'

    def _compute_margin(self, cr, uid, ids, name, arg, context=None):
        if context is None:
            context = {}
        res = {}
        # we need an up-to-date price_subtotal
        # We cannot read il.price_subtotal, because it may be out-of-date
        # (I saw that with invoices in foreign currency)
        price_subtotal = self._amount_line(cr, uid, ids, name, arg, context)
        for il in self.browse(cr, uid, ids, context=context):
            standard_price_inv_cur = 0.0
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            margin_rate = 0.0
            if (
                    il.invoice_id and
                    il.invoice_id.type in ('out_invoice', 'out_refund')):
                # it works in _get_current_rate
                # even if we set date = False in context
                # standard_price_inv_cur is in the UoM of the invoice line

                rco = self.pool['res.currency']
                ctx_currency = context.copy()
                if il.invoice_id.date_invoice:
                    ctx_currency['date'] = il.invoice_id.date_invoice
                standard_price_inv_cur =\
                    rco.compute(
                        cr, uid, il.invoice_id.company_id.currency_id.id,
                        il.invoice_id.currency_id.id,
                        il.standard_price_company_currency,
                        context=ctx_currency)
                margin_inv_cur =\
                    price_subtotal[il.id] - il.quantity * standard_price_inv_cur
                margin_comp_cur = rco.compute(
                    cr, uid, il.invoice_id.currency_id.id,
                    il.invoice_id.company_id.currency_id.id,
                    margin_inv_cur, context=ctx_currency)
                if price_subtotal[il.id]:
                    margin_rate = 100 * margin_inv_cur / price_subtotal[il.id]
                # for a refund, margin should be negative
                # but margin rate should stay positive
                if il.invoice_id.type == 'out_refund':
                    margin_inv_cur *= -1
                    margin_comp_cur *= -1
            res[il.id] = {
                'standard_price_invoice_currency': standard_price_inv_cur,
                'margin_invoice_currency': margin_inv_cur,
                'margin_company_currency': margin_comp_cur,
                'margin_rate': margin_rate,
                }
        return res

    def _get_lines_from_invoices(self, cr, uid, ids, context=None):
        return self.pool['account.invoice.line'].search(
            cr, uid, [('invoice_id', 'in', ids)], context=context)

    _columns = {
        'standard_price_company_currency': fields.float(
            'Cost Price per Unit in Company Currency', readonly=True,
            digits_compute=dp.get_precision('Product Price'),
            help="Cost price in company currency in the unit of measure "
            "of the invoice line (which may be different from the unit "
            "of measure of the product)."),
        'standard_price_invoice_currency': fields.function(
            _compute_margin, string='Cost Price per Unit in Invoice Currency',
            type='float', readonly=True, multi='il-margin', store={
                'account.invoice.line': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'standard_price_company_currency',
                        'quantity',
                        'price_unit',
                        'discount',
                        'invoice_line_tax_id'], 10),
                'account.invoice': (
                    _get_lines_from_invoices, [
                        'type',
                        'currency_id',
                        'date_invoice',
                        'company_id'], 20),
                },
            digits_compute=dp.get_precision('Product Price'),
            help="Cost price in invoice currency in the unit of measure "
            "of the invoice line"),
        'margin_invoice_currency': fields.function(
            _compute_margin, string='Margin in Invoice Currency',
            type='float', readonly=True, multi='il-margin', store={
                'account.invoice.line': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'standard_price_company_currency',
                        'quantity',
                        'price_unit',
                        'discount',
                        'invoice_line_tax_id'], 10),
                'account.invoice': (
                    _get_lines_from_invoices, [
                        'type',
                        'currency_id',
                        'date_invoice',
                        'company_id'], 20),
                },
            digits_compute=dp.get_precision('Account')),
        'margin_company_currency': fields.function(
            _compute_margin, type='float',
            string='Margin in Company Currency', readonly=True,
            multi='il-margin', store={
                'account.invoice.line': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'standard_price_company_currency',
                        'quantity',
                        'price_unit',
                        'discount',
                        'invoice_line_tax_id'], 10),
                'account.invoice': (
                    _get_lines_from_invoices, [
                        'type',
                        'currency_id',
                        'date_invoice',
                        'company_id'], 20),
                },
            digits_compute=dp.get_precision('Account')),
        'margin_rate': fields.function(
            _compute_margin, type='float',
            string="Margin Rate", readonly=True, multi='il-margin', store={
                'account.invoice.line': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'standard_price_company_currency',
                        'quantity',
                        'price_unit',
                        'discount',
                        'invoice_line_tax_id'], 10),
                'account.invoice': (
                    _get_lines_from_invoices, [
                        'type',
                        'currency_id',
                        'date_invoice',
                        'company_id'], 20),
                },
            digits=(16, 2),
            help="Margin rate in percentage of the sale price"),
        }

    # We want to copy standard_price on invoice line for customer
    # invoice/refunds. We can't do that via on_change of product_id,
    # because it is not always played when invoice is created from code
    # => we inherit write/create
    # We write standard_price_company_currency even on supplier invoice/refunds
    # because we don't have access to the 'type' of the invoice
    def create(self, cr, uid, vals, context=None):
        if (
                vals.get('product_id') and
                'standard_price_company_currency' not in vals):
            pp = self.pool['product.product'].browse(
                cr, uid, vals['product_id'], context=context)
            std_price = pp.standard_price
            inv_uom_id = vals.get('uos_id')
            if inv_uom_id and inv_uom_id != pp.uom_id.id:
                std_price = self.pool['product.uom']._compute_price(
                    cr, uid, pp.uom_id.id, std_price, inv_uom_id)
            vals['standard_price_company_currency'] = std_price
        return super(AccountInvoiceLine, self).create(
            cr, uid, vals, context=context)

    def write(self, cr, uid, ids, vals, context=None):
        """This code can seem a bit strange with the super() inside
        the loop, but it is required if we want to support all scenarios,
        including very strange scenarios where you write a uos_id on
        several lines with different products, etc...
        OK, these scenarios will probably never happen, but I prefer
        to make sure that the code is right and works in all
        scenarios
        """
        if not vals:
            vals = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if 'product_id' in vals or 'uos_id' in vals:
            for il in self.browse(cr, uid, ids, context=context):
                if 'product_id' in vals:
                    if vals.get('product_id'):
                        pp = self.pool['product.product'].browse(
                            cr, uid, vals['product_id'], context=context)
                    else:
                        pp = False
                else:
                    pp = il.product_id or False
                # uos_id is NOT a required field
                if 'uos_id' in vals:
                    if vals.get('uos_id'):
                        inv_uom = self.pool['product.uom'].browse(
                            cr, uid, vals['uos_id'], context=context)
                    else:
                        inv_uom = False
                else:
                    inv_uom = il.uos_id or False
                std_price = 0.0
                if pp:
                    std_price = pp.standard_price
                    if inv_uom and inv_uom != pp.uom_id:
                        std_price = self.pool['product.uom']._compute_price(
                            cr, uid, pp.uom_id.id, std_price, inv_uom.id)
                vals_line = vals.copy()
                vals_line['standard_price_company_currency'] = std_price
                super(AccountInvoiceLine, self).write(
                    cr, uid, [il.id], vals_line, context=context)
                return True
        else:
            return super(AccountInvoiceLine, self).write(
                cr, uid, ids, vals, context=context)


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def _compute_margin(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for inv in self.browse(cr, uid, ids, context=context):
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            if inv.type in ('out_invoice', 'out_refund'):
                for il in inv.invoice_line:
                    margin_inv_cur += il.margin_invoice_currency
                    margin_comp_cur += il.margin_company_currency
            res[inv.id] = {
                'margin_invoice_currency': margin_inv_cur,
                'margin_company_currency': margin_comp_cur,
                }
        return res

    def _get_invoices_from_inv_lines(self, cr, uid, ids, context=None):
        return self.pool['account.invoice'].search(
            cr, uid, [('invoice_line', 'in', ids)], context=context)

    _columns = {
        'margin_invoice_currency': fields.function(
            _compute_margin, type='float',
            string='Margin in Invoice Currency',
            readonly=True, multi='inv-margin',
            digits_compute=dp.get_precision('Account'), store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'type', 'currency_id'], 10),
                'account.invoice.line': (
                    _get_invoices_from_inv_lines, [
                        'margin_company_currency'], 20),
                }),
        'margin_company_currency': fields.function(
            _compute_margin, type='float',
            string='Margin in Company Currency',
            readonly=True, multi='inv-margin',
            digits_compute=dp.get_precision('Account'), store={
                'account.invoice': (
                    lambda self, cr, uid, ids, c={}: ids, [
                        'type', 'currency_id'], 10),
                'account.invoice.line': (
                    _get_invoices_from_inv_lines, [
                        'margin_company_currency'], 20),
                }),
        }
