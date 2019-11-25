# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_round


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sale_id = fields.Many2one('sale.order', string='Sale Order')

    def action_validate_invoice_payment(self):
        if self.sale_id:
            self.post()
        else:
            return super(AccountPayment, self).\
                action_validate_invoice_payment()

    def _get_counterpart_move_line_vals(self, invoice=False):
        res = super(AccountPayment, self)._get_counterpart_move_line_vals(
            invoice=invoice)
        if self.sale_id:
            res['sale_id'] = self.sale_id.id
        return res


class AccountAbstractPayment(models.AbstractModel):
    _inherit = "account.abstract.payment"

    def default_get(self, fields_list):
        res = super(AccountAbstractPayment, self).default_get(fields_list)
        if (
                self._context.get('active_model') == 'sale.order' and
                self._context.get('active_id')):
            so = self.env['sale.order'].browse(self._context['active_id'])
            res.update({
                'amount': so.amount_total,
                'currency_id': so.currency_id.id,
                'payment_type': 'inbound',
                'partner_id': so.partner_invoice_id.commercial_partner_id.id,
                'partner_type': 'customer',
                'communication': so.name,
                'sale_id': so.id,
                })
        return res

    def _compute_payment_amount(self, invoices=None, currency=None):
        amount = super(AccountAbstractPayment, self)._compute_payment_amount(
            invoices=invoices, currency=currency)
        if self.sale_id:
            payment_currency = currency
            if not payment_currency:
                payment_currency = self.sale_id.currency_id
            amount = float_round(
                self.sale_id.amount_total - self.sale_id.amount_down_payment,
                precision_rounding=payment_currency.rounding)
        return amount
