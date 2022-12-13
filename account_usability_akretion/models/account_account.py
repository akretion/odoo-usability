# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


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
