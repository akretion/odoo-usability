# Copyright 2018-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    margin = fields.Float(string='Margin', readonly=True)
    # why digits=0 ??? Why is it like that in the native "account" module
    user_currency_margin = fields.Float(
        string="Margin", compute='_compute_user_currency_margin', digits=0)

    _depends = {
        'account.invoice': [
            'account_id', 'amount_total_company_signed',
            'commercial_partner_id', 'company_id',
            'currency_id', 'date_due', 'date_invoice', 'fiscal_position_id',
            'journal_id', 'number', 'partner_bank_id', 'partner_id',
            'payment_term_id', 'residual', 'state', 'type', 'user_id',
        ],
        'account.invoice.line': [
            'account_id', 'invoice_id', 'price_subtotal', 'product_id',
            'quantity', 'uom_id', 'account_analytic_id',
            'margin_company_currency',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @api.depends('currency_id', 'date', 'margin')
    def _compute_user_currency_margin(self):
        user_currency = self.env.user.company_id.currency_id
        currency_rate = self.env['res.currency.rate'].search([
            ('rate', '=', 1),
            '|',
            ('company_id', '=', self.env.user.company_id.id),
            ('company_id', '=', False)], limit=1)
        base_currency = currency_rate.currency_id
        for record in self:
            date = record.date or fields.Date.today()
            company = record.company_id
            record.user_currency_margin = base_currency._convert(
                record.margin, user_currency, company, date)

    # TODO check for refunds
    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += ", SUM(ail.margin_company_currency) AS margin"
        return select_str

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += ", sub.margin AS margin"
        return select_str
