# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Invoice Partner Bank Usability module for Odoo
#    Copyright (C) 2013-2016 Akretion (http://www.akretion.com)
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

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_out_invoice_partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Default Bank Account for Customer Invoices',
        copy=False, ondelete='restrict',
        help="This is the bank account of your company that will be selected "
        "by default when you create a customer invoice.")


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def invoice_out_default_bank_account(self):
        partner_bank_id = False
        if self._context.get('type') == 'out_invoice' or \
                self._context.get('inv_type') == 'out_invoice':
            partner_bank_id = self.env.user.company_id.\
                default_out_invoice_partner_bank_id.id or False
        return partner_bank_id

    partner_bank_id = fields.Many2one(default=invoice_out_default_bank_account)
