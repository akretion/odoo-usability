# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError, ValidationError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    hide_bank_statement_balance = fields.Boolean(
        string='Hide Bank Statement Balance',
        help="You may want to enable this option when your bank "
        "journal is generated from a bank statement file that "
        "doesn't handle start/end balance (QIF for instance) and "
        "you don't want to enter the start/end balance manually: it "
        "will prevent the display of wrong information in the accounting "
        "dashboard and on bank statements.")

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
