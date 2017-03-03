# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Move Line Filter Wizard module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
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


class AccountMoveLineFilterWizard(models.TransientModel):
    _name = 'account.move.line.filter.wizard'
    _description = 'Wizard for easy and fast access to account move lines'

    partner_id = fields.Many2one(
        'res.partner', string='Partner', domain=[('parent_id', '=', False)])
    account_id = fields.Many2one(
        'account.account', string='Account',
        domain=[('type', 'not in', ('view', 'closed'))], required=True)
    account_reconcile = fields.Boolean(related='account_id.reconcile')
    reconcile = fields.Selection([
        ('unreconciled', 'Unreconciled'),
        ('reconciled', 'Fully Reconciled'),
        ('partial_reconciled', 'Partially Reconciled'),
        ], string='Reconciliation Filter')

    @api.onchange('partner_id')
    def partner_id_change(self):
        if self.partner_id:
            if self.partner_id.customer:
                self.account_id =\
                    self.partner_id.property_account_receivable.id
            else:
                self.account_id = self.partner_id.property_account_payable.id

    @api.multi
    def go(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account', 'action_account_moves_all_a')
        action['context'] = {
            'search_default_account_id': [self.account_id.id],
            'journal_show_code_only': True,
            }
        if self.partner_id:
            action['context']['search_default_partner_id'] =\
                [self.partner_id.id]
        if self.reconcile:
            action['context']['search_default_%s' % self.reconcile] = True
        return action
