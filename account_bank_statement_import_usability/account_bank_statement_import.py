# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountBankStatementImport(models.TransientModel):
    _inherit = 'account.bank.statement.import'

    def _check_journal_bank_account(self, journal, account_number):
        if account_number in journal.bank_account_id.sanitized_acc_number:
            return True
        return False


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    # When we use the import of bank statement via files,
    # the start/end_balance is usually computed from the lines itself
    # because we don't have the 'real' information in the file
    # But, in the module account_bank_statement_import, in the method
    # _create_bank_statement(), the bank statement lines already present in
    # Odoo are filtered out, but the start/end balance is not adjusted,
    # so the user has to manually modifiy it the close the bank statement
    # I think the solution is just to remove the start/end balance system
    # on the bank statement when we use the file import
    # This code is present in the 'account' module, but I override it here
    # and not in account_usability because the users who don't have
    # account_bank_statement_import may want to keep start/end balance
    @api.multi
    def _balance_check(self):
        return True
