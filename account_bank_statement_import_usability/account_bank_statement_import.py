# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Bank Statement Import Usability module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class AccountBankStatementImport(models.TransientModel):
    """Extend model account.bank.statement."""
    _inherit = 'account.bank.statement.import'

    @api.model
    def _find_bank_account_id(self, account_number):
        """ Get res.partner.bank ID """
        bank_account_id = None
        if account_number and len(account_number) > 4:
            self._cr.execute("select id from res_partner_bank where replace(replace(acc_number,' ',''),'-','') like %s and journal_id is not null", ('%' + account_number + '%',))
            bank_account_ids = [id[0] for id in self._cr.fetchall()]
            if bank_account_ids:
                bank_account_id = bank_account_ids[0]
        return bank_account_id
