# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPaymentRegisterSale(models.TransientModel):
    _name = 'account.payment.register.sale'
    _description = "Register a payment from a sale.order"
    _check_company_auto = True

    sale_id = fields.Many2one(
        "sale.order", string="Sale Order",
        check_company=True, readonly=True, required=True)
    company_id = fields.Many2one('res.company', required=True)
    journal_id = fields.Many2one(
        'account.journal', string="Journal", check_company=True, required=True,
        domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]")
    amount = fields.Monetary(required=True)
    currency_id = fields.Many2one('res.currency', required=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    ref = fields.Char()

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self._context.get('active_model') == 'sale.order' and self._context.get('active_id'):
            sale = self.env['sale.order'].browse(self._context['active_id'])
            res.update({
                'sale_id': sale.id,
                'company_id': sale.company_id.id,
                'amount': sale.amount_total,
                'currency_id': sale.currency_id.id,
                })
        return res

    def run(self):
        self.ensure_one()
        pay_vals = {
            'company_id': self.company_id.id,
            'sale_id': self.sale_id.id,
            'date': self.date,
            'amount': self.amount,
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'ref': self.ref,
            'journal_id': self.journal_id.id,
            'currency_id': self.currency_id.id,
            'partner_id': self.sale_id.partner_invoice_id.commercial_partner_id.id,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            }
        payment = self.env['account.payment'].create(pay_vals)
        payment.action_post()

    @api.onchange("journal_id")
    def journal_id_change(self):
        if (
                self.journal_id and
                self.journal_id.currency_id and
                self.journal_id.currency_id != self.currency_id):
            self.currency_id = self.journal_id.currency_id.id
