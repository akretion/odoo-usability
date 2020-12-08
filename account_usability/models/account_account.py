# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
import logging

logger = logging.getLogger(__name__)


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.depends('name', 'code')
    def name_get(self):
        if self._context.get('account_account_show_code_only'):
            res = []
            for record in self:
                res.append((record.id, record.code))
            return res
        else:
            return super().name_get()

    # https://github.com/odoo/odoo/issues/23040
    # TODO mig to v14 ?
    def fix_bank_account_types(self):
        aao = self.env['account.account']
        companies = self.env['res.company'].search([])
        if len(companies) > 1:
            self = self.sudo()
        logger.info("START the script 'fix bank and cash account types'")
        bank_type = self.env.ref('account.data_account_type_liquidity')
        asset_type = self.env.ref('account.data_account_type_current_assets')
        journals = self.env['account.journal'].search(
            [('type', 'in', ('bank', 'cash'))], order='company_id')
        journal_accounts_bank_type = aao
        for journal in journals:
            for account in [
                    journal.default_credit_account_id,
                    journal.default_debit_account_id]:
                if account:
                    if account.user_type_id != bank_type:
                        account.user_type_id = bank_type.id
                        logger.info(
                            'Company %s: Account %s updated to Bank '
                            'and Cash type',
                            account.company_id.display_name, account.code)
                    if account not in journal_accounts_bank_type:
                        journal_accounts_bank_type += account
        accounts = aao.search([
            ('user_type_id', '=', bank_type.id)], order='company_id, code')
        for account in accounts:
            if account not in journal_accounts_bank_type:
                account.user_type_id = asset_type.id
                logger.info(
                    'Company %s: Account %s updated to Current Asset type',
                    account.company_id.display_name, account.code)
        logger.info("END of the script 'fix bank and cash account types'")
        return True
