# Copyright 2019-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_ids = fields.One2many(
        'account.payment', 'sale_id', string='Advance Payments',
        readonly=True)
    amount_down_payment = fields.Monetary(
        compute='_compute_amount_down_payment', string='Down Payment Amount')
    # amount_residual : only used to hide 'Register Payment' button
    amount_residual = fields.Monetary(
        compute='_compute_amount_down_payment', string='Residual')

    @api.depends(
        'payment_ids.amount', 'payment_ids.currency_id', 'payment_ids.date',
        'payment_ids.state', 'currency_id')
    def _compute_amount_down_payment(self):
        for sale in self:
            down_payment = 0.0
            sale_currency = sale.currency_id
            prec_rounding = sale_currency.rounding or 0.01
            for payment in sale.payment_ids:
                if payment.payment_type == 'inbound' and payment.state == 'posted':
                    down_payment += payment.currency_id._convert(
                        payment.amount, sale_currency, sale.company_id,
                        payment.date)
            down_payment = float_round(
                down_payment, precision_rounding=prec_rounding)
            sale.amount_down_payment = down_payment
            sale.amount_residual = float_round(
                sale.amount_total - down_payment, precision_rounding=prec_rounding)
