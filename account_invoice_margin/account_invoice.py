# Copyright 2015-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


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
    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency', readonly=True, store=True,
        compute='_compute_margin', currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency', readonly=True, store=True,
        compute='_compute_margin', currency_field='company_currency_id')
    margin_rate = fields.Float(
        string="Margin Rate", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.depends(
        'standard_price_company_currency', 'invoice_id.currency_id',
        'invoice_id.type', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'quantity', 'price_subtotal')
    def _compute_margin(self):
        for il in self:
            standard_price_inv_cur = 0.0
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            margin_rate = 0.0
            inv = il.invoice_id
            if inv and inv.type in ('out_invoice', 'out_refund'):
                # it works in _get_current_rate
                # even if we set date = False in context
                # standard_price_inv_cur is in the UoM of the invoice line
                date = inv._get_currency_rate_date() or\
                    fields.Date.context_today(self)
                company = inv.company_id
                company_currency = company.currency_id
                standard_price_inv_cur =\
                    company_currency._convert(
                        il.standard_price_company_currency,
                        inv.currency_id, company, date)
                margin_inv_cur =\
                    il.price_subtotal - il.quantity * standard_price_inv_cur
                margin_comp_cur = inv.currency_id._convert(
                    margin_inv_cur, company_currency, company, date)
                if il.price_subtotal:
                    margin_rate = 100 * margin_inv_cur / il.price_subtotal
                # for a refund, margin should be negative
                # but margin rate should stay positive
                if inv.type == 'out_refund':
                    margin_inv_cur *= -1
                    margin_comp_cur *= -1
            il.standard_price_invoice_currency = standard_price_inv_cur
            il.margin_invoice_currency = margin_inv_cur
            il.margin_company_currency = margin_comp_cur
            il.margin_rate = margin_rate

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
            inv_uom_id = vals.get('uom_id')
            if inv_uom_id and inv_uom_id != pp.uom_id.id:
                inv_uom = self.env['uom.uom'].browse(inv_uom_id)
                std_price = pp.uom_id._compute_price(
                    std_price, inv_uom)
            vals['standard_price_company_currency'] = std_price
        return super(AccountInvoiceLine, self).create(vals)

    def write(self, vals):
        if not vals:
            vals = {}
        if 'product_id' in vals or 'uom_id' in vals:
            for il in self:
                if 'product_id' in vals:
                    if vals.get('product_id'):
                        pp = self.env['product.product'].browse(
                            vals['product_id'])
                    else:
                        pp = False
                else:
                    pp = il.product_id or False
                # uom_id is NOT a required field
                if 'uom_id' in vals:
                    if vals.get('uom_id'):
                        inv_uom = self.env['uom.uom'].browse(
                            vals['uom_id'])
                    else:
                        inv_uom = False
                else:
                    inv_uom = il.uom_id or False
                std_price = 0.0
                if pp:
                    std_price = pp.standard_price
                    if inv_uom and inv_uom != pp.uom_id:
                        std_price = pp.uom_id._compute_price(
                            std_price, inv_uom)
                il.write({'standard_price_company_currency': std_price})
        return super(AccountInvoiceLine, self).write(vals)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency',
        compute='_compute_margin', store=True, readonly=True,
        currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency',
        compute='_compute_margin', store=True, readonly=True,
        currency_field='company_currency_id')

    @api.depends(
        'type',
        'invoice_line_ids.margin_invoice_currency',
        'invoice_line_ids.margin_company_currency')
    def _compute_margin(self):
        res = self.env['account.invoice.line'].read_group(
            [('invoice_id', 'in', self.ids)],
            ['invoice_id', 'margin_invoice_currency',
             'margin_company_currency'],
            ['invoice_id'])
        for re in res:
            if re['invoice_id']:
                inv = self.browse(re['invoice_id'][0])
                if inv.type in ('out_invoice', 'out_refund'):
                    inv.margin_invoice_currency = re['margin_invoice_currency']
                    inv.margin_company_currency = re['margin_company_currency']
