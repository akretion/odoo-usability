# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    hide_bank_statement_balance = fields.Boolean(
        string='Hide and Disable Bank Statement Balance',
        help="When this option is enabled, the start and end balance is "
        "not displayed on the bank statement form view, and the check of "
        "the end balance vs the real end balance is disabled. When you enable "
        "this option, you process the statement lines without considering "
        "the start/end balance and you regularly check the accounting balance "
        "of the bank account vs the amount of your bank account "
        "(the 2 processes are managed separately)."
        )
    # Used to set default user_type_id on account fields via context
    account_type_current_assets_id = fields.Many2one(
        'account.account.type',
        default=lambda self: self.env.ref('account.data_account_type_current_assets').id)

    # SQL constraint in the 'account' module: unique(code, name, company_id) !!!
    _sql_constraints = [(
        'code_unique', 'unique(code, company_id)',
        'Another journal already has this code in this company!')]

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

#    @api.constrains('default_credit_account_id', 'default_debit_account_id')
#    def _check_account_type_on_bank_journal(self):
#        bank_acc_type = self.env.ref('account.data_account_type_liquidity')
#        for jrl in self:
#            if jrl.type in ('bank', 'cash'):
#                if (
#                        jrl.default_debit_account_id and
#                        jrl.default_debit_account_id.user_type_id !=
#                        bank_acc_type):
#                    raise ValidationError(_(
#                        "On journal '%s', the default debit account '%s' "
#                        "should be configured with Type = 'Bank and Cash'.")
#                        % (jrl.display_name,
#                           jrl.default_debit_account_id.display_name))
#                if (
#                        jrl.default_credit_account_id and
#                        jrl.default_credit_account_id.user_type_id !=
#                        bank_acc_type):
#                    raise ValidationError(_(
#                        "On journal '%s', the default credit account '%s' "
#                        "should be configured with Type = 'Bank and Cash'.")
#                        % (jrl.display_name,
#                           jrl.default_credit_account_id.display_name))
