# Copyright 2015-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    hide_bank_statement_balance = fields.Boolean(
        string='Hide and Disable Bank Statement Balance', default=True,
        help="When this option is enabled, the start and end balance is "
        "not displayed on the bank statement form view, and the check of "
        "the end balance vs the real end balance is disabled. When you enable "
        "this option, you process the statement lines without considering "
        "the start/end balance and you regularly check the accounting balance "
        "of the bank account vs the amount of your bank account."
        )
    bank_currency_id = fields.Many2one("res.currency", compute="_compute_bank_default_account_balance", string="Display Currency for Bank Journal")
    bank_default_account_balance = fields.Monetary(
        compute="_compute_bank_default_account_balance", string="Balance in GL (float)", currency_field="bank_currency_id")
    bank_default_account_balance_str = fields.Char(
        compute="_compute_bank_default_account_balance", string="Balance in GL")

    @api.depends('name', 'currency_id', 'company_id', 'code')
    @api.depends_context('journal_show_code_only')
    def _compute_display_name(self):
        if self._context.get('journal_show_code_only'):
            for journal in self:
                journal.display_name = journal.code
        else:
            for journal in self:
                name = f"[{journal.code}] {journal.name}"
                if (
                        journal.currency_id and
                        journal.currency_id != journal.company_id.currency_id):
                    name = f"{name} ({journal.currency_id.name})"
                journal.display_name = name

    def _compute_bank_default_account_balance(self):
        rg_res = self.env['account.move.line']._read_group(
            domain=[
                ('account_id', 'in', tuple(self.default_account_id.ids)),
                ('display_type', 'not in', ('line_section', 'line_note')),
                ('parent_state', '=', 'posted'),
            ],
            groupby=['account_id'],
            aggregates=['balance:sum', 'amount_currency:sum'],
        )
        mapped_data = {account.id: (balance, amount_currency) for (account, balance, amount_currency) in rg_res}
        for journal in self:
            balance = 0.0
            currency = False
            balance_str = ''
            if journal.type in ('bank', 'cash', 'credit') and journal.default_account_id:
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

#    def open_outstanding_payments(self):
#        self.ensure_one()
#        action = self.env["ir.actions.actions"]._for_xml_id(
#            "account.action_account_moves_all")
#        action['domain'] = [
#            ('account_id', 'in', (self.payment_debit_account_id.id, self.payment_credit_account_id.id)),
#            ('journal_id', '=', self.id),
#            ('display_type', 'not in', ('line_section', 'line_note')),
#            ('parent_state', '!=', 'cancel'),
#            ]
#        action['context'] = {
#            'search_default_unreconciled': True,
#            'search_default_posted': True,
#            }
#        return action
