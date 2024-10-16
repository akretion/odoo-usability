# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountPaymentOrder(models.Model):
    _inherit = "account.payment.order"

    def _prepare_move_line_partner_account(self, bank_line):
        vals = super()._prepare_move_line_partner_account(bank_line)
        if not bank_line.payment_line_ids[0].move_line_id:
            vals.update({
                'account_id': bank_line.payment_line_ids[0].account_id.id,
                'analytic_account_id': bank_line.payment_line_ids[0].analytic_account_id.id or False,
                })
        return vals
