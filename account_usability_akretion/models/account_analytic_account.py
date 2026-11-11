# Copyright 2015-2026 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.depends_context('analytic_account_show_code_only')
    def _compute_display_name(self):
        if self._context.get('analytic_account_show_code_only'):
            for rec in self:
                rec.display_name = rec.code or rec.name
        else:
            return super()._compute_display_name()

    _code_company_unique = models.UniqueIndex(
        "(code, company_id)",
        "An analytic account with the same code already exists in the same company!"
        )
