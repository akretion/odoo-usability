# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def get_reconciliation_proposition(self, excluded_ids=None):
        self.ensure_one()
        return self.env['account.move.line']
