# Copyright 2015-2022 Akretion (http://www.akretion.com)
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

    @api.depends(
        'name', 'currency_id', 'company_id', 'company_id.currency_id', 'code')
    def name_get(self):
        res = []
        if self._context.get('journal_show_code_only'):
            for journal in self:
                res.append((journal.id, journal.code))
            return res
        else:
            for journal in self:
                name = "[%s] %s" % (journal.code, journal.name)
                if (
                        journal.currency_id and
                        journal.currency_id != journal.company_id.currency_id):
                    name = "%s (%s)" % (name, journal.currency_id.name)
                res.append((journal.id, name))
            return res

    def open_outstanding_payments(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_account_moves_all")
        action['domain'] = [
            ('account_id', 'in', (self.payment_debit_account_id.id, self.payment_credit_account_id.id)),
            ('journal_id', '=', self.id),
            ('display_type', 'not in', ('line_section', 'line_note')),
            ('parent_state', '!=', 'cancel'),
            ]
        action['context'] = {
            'search_default_unreconciled': True,
            'search_default_posted': True,
            }
        return action

    # field used in journal dashboard for bank journals
    # compute account_balance like in v14, using accounting and
    # NOT bank statement balance_start/balance_end
    def _compute_current_statement_balance(self):
        query_result = self._get_journal_dashboard_bank_running_balance()
        for journal in self:
            journal.has_statement_lines = query_result.get(journal.id)[0]
            journal.current_statement_balance = journal._get_journal_bank_account_balance()[0]
