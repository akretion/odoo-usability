# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 EduSense BV (<http://www.edusense.nl>).
#              (C) 2011 - 2013 Therp BV (<http://therp.nl>).
#              (C) 2014 Akretion (www.akretion.com)
#
#    All other contributions are (C) by their respective contributors
#
#    All Rights Reserved
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

from openerp.osv import orm, fields


class PaymentMode(orm.Model):
    _inherit = "payment.mode"

    _columns = {
        'transfer_account_id': fields.many2one(
            'account.account', 'Transfer account',
            domain=[('type', '=', 'other'), ('reconcile', '=', True)],
            help='Pay off lines in sent orders with a move on this '
            'account. You can only select accounts of type regular '
            'that are marked for reconciliation'),
        'transfer_journal_id': fields.many2one(
            'account.journal', 'Transfer journal',
            help='Journal to write payment entries when confirming '
            'a debit order of this mode'),
        'transfer_move_option': fields.selection([
            ('date', 'One move per payment date'),
            ('line', 'One move per payment line'),
            ], 'Transfer move option')
    }

    _defaults = {
        'transfer_move_option': 'date',
    }
