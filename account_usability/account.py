# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Usability module for Odoo
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

from openerp import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    origin = fields.Char(track_visibility='onchange')
    supplier_invoice_number = fields.Char(track_visibility='onchange')
    internal_number = fields.Char(track_visibility='onchange')
    reference = fields.Char(track_visibility='onchange')
    sent = fields.Boolean(track_visibility='onchange')
    date_invoice = fields.Date(track_visibility='onchange')
    date_due = fields.Date(track_visibility='onchange')
    payment_term = fields.Many2one(track_visibility='onchange')
    period_id = fields.Many2one(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    partner_bank_id = fields.Many2one(track_visibility='onchange')
    fiscal_position = fields.Many2one(track_visibility='onchange')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.onchange('credit')
    def _credit_onchange(self):
        if self.credit and self.debit:
            self.debit = 0

    @api.onchange('debit')
    def _debit_onchange(self):
        if self.debit and self.credit:
            self.credit = 0


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    # Disable guessing for reconciliation
    # because my experience with several customers shows that it is a problem
    # in the following scenario : move line 'x' has been "guessed" by OpenERP
    # to be reconciled with a statement line 'Y' at the end of the bank statement,
    # but it is a mistake because it should be reconciled with statement line 'B'
    # at the beginning of the bank statement
    # When the user is on statement line 'B', he tries to select
    # move line 'x', but it can't find it... because it is already "reserved"
    # by the guess of OpenERP for statement line 'Y' ! To solve this problem, the
    # user must go to statement line 'Y' and unselect move line 'x' and then come
    # back on statement line 'B' and select move line 'A'... but non super-expert
    # users can't do that because it is impossible to figure out that the fact that
    # the user can't find move line 'x' is caused by this.
    # Set search_reconciliation_proposition to False by default
    def get_data_for_reconciliations(
            self, cr, uid, ids, excluded_ids=None,
            search_reconciliation_proposition=False, context=None):
        return super(AccountBankStatementLine ,self).get_data_for_reconciliations(
            cr, uid, ids, excluded_ids=excluded_ids,
            search_reconciliation_proposition=search_reconciliation_proposition,
            context=context)
