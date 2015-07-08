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
