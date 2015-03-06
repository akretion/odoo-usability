# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Voucher Default Amount module for Odoo
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

from openerp import models


class AccountVoucher(models.Model):
    _inherit = 'account.voucher'

    def onchange_partner_id(
            self, cr, uid, ids, partner_id, journal_id, amount,
            currency_id, ttype, date, context=None):
        res = super(AccountVoucher, self).onchange_partner_id(
            cr, uid, ids, partner_id, journal_id, amount,
            currency_id, ttype, date, context=context)
        if (
                partner_id and not amount and ttype == 'receipt'
                and res.get('value') and res['value'].get('line_cr_ids')):
            total_open_bal = 0.0
            for line in res['value']['line_cr_ids']:
                total_open_bal += line['amount_unreconciled']
            res['value']['amount'] = total_open_bal
        return res
