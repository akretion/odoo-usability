# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    # field displayed in pos.order list view
    payments_char = fields.Char(
        string="Payment Methods", compute="_compute_payments_char", store=True)

    @api.depends('payment_ids')
    def _compute_payments_char(self):
        for order in self:
            payments = set()
            for pay in order.payment_ids:
                if pay.payment_method_id.name:
                    # unfortunately, 'name' of pos.payment.method is translate=True
                    payments.add(pay.payment_method_id.name)
            order.payments_char = ', '.join(payments)
