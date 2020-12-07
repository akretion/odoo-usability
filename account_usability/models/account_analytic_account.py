# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def name_get(self):
        if self._context.get('analytic_account_show_code_only'):
            res = []
            for record in self:
                res.append((record.id, record.code or record.name))
            return res
        else:
            return super().name_get()

    _sql_constraints = [(
        'code_company_unique',
        'unique(code, company_id)',
        'An analytic account with the same code already '
        'exists in the same company!')]
