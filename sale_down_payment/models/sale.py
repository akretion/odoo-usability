# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_line_ids = fields.One2many(
        'account.move.line', 'sale_id', string='Advance Payments',
        readonly=True)
    amount_down_payment = fields.Monetary(
        compute='_compute_amount_down_payment', string='Down Payment Amount')

    @api.depends(
        'payment_line_ids.credit', 'payment_line_ids.debit',
        'payment_line_ids.amount_currency', 'payment_line_ids.currency_id',
        'payment_line_ids.date', 'currency_id')
    def _compute_amount_down_payment(self):
        for sale in self:
            down_payment = 0.0
            sale_currency = sale.pricelist_id.currency_id
            if sale_currency == sale.company_id.currency_id:
                for pl in sale.payment_line_ids:
                    down_payment -= pl.balance
            else:
                for pl in sale.payment_line_ids:
                    if (
                            pl.currency_id and
                            pl.currency_id == sale_currency and
                            pl.amount_currency):
                        down_payment -= pl.amount_currency
                    else:
                        down_payment -= sale.company_id.currency_id._convert(
                            pl.balance, sale_currency, sale.company_id,
                            pl.date)
            sale.amount_down_payment = down_payment
