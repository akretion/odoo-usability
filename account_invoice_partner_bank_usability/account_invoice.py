# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Partner Bank Usability module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
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

from openerp.osv import orm


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    def invoice_out_get_first_partner_bank(self, cr, uid, context=None):
        '''Get the first bank account of your company on customer invoice
        if your company only has one bank account'''
        if context is None:
            context = {}
        res_partner_bank_id = False
        if context.get('type') == 'out_invoice' or \
                context.get('inv_type') == 'out_invoice':
            cur_user = self.pool['res.users'].browse(
                cr, uid, uid, context=context)
            partner_banks = cur_user.company_id.partner_id.bank_ids
            if partner_banks and len(partner_banks) == 1:
                res_partner_bank_id = partner_banks[0].id
        return res_partner_bank_id

    _defaults = {
        'partner_bank_id': invoice_out_get_first_partner_bank,
    }
