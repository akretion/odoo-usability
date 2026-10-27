# Copyright 2026 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    bank_currency_id = fields.Many2one("res.currency", compute="_compute_bank_default_account_balance", string="Display Currency for Bank Journal")
    bank_default_account_balance = fields.Monetary(
        compute="_compute_bank_default_account_balance", string="Balance in GL (float)", currency_field="bank_currency_id")
    bank_default_account_balance_str = fields.Char(
        compute="_compute_bank_default_account_balance", string="Balance in GL (string)")

    def _compute_bank_default_account_balance(self):
        rg_res = self.env['account.move.line'].read_group(
            [
                ('account_id', 'in', tuple(self.default_account_id.ids)),
                ('display_type', 'not in', ('line_section', 'line_note')),
                ('parent_state', '=', 'posted'),
            ],
            ['account_id', 'balance:sum', 'amount_currency:sum'],
            ['account_id'],
        )
        mapped_data = {x['account_id'][0]: (x['balance'], x['amount_currency']) for x in rg_res}
        for journal in self:
            balance = 0.0
            currency = False
            balance_str = ''
            if journal.type in ('bank', 'cash') and journal.default_account_id:
                balance = 0.0
                if journal.currency_id and journal.currency_id != journal.company_id.currency_id:
                    balance = mapped_data.get(journal.default_account_id.id, (0.0, 0.0))[1]
                    currency = journal.currency_id
                else:
                    balance = mapped_data.get(journal.default_account_id.id, (0.0, 0.0))[0]
                    currency = journal.company_id.currency_id
                balance_str = currency.format(balance)
            journal.bank_currency_id = currency and currency.id or False
            journal.bank_default_account_balance = balance
            journal.bank_default_account_balance_str = balance_str
