# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountMoveLineFilterWizard(models.TransientModel):
    _name = 'account.move.line.filter.wizard'
    _description = 'Wizard for easy and fast access to account move lines'

    partner_id = fields.Many2one(
        'res.partner', string='Partner', domain=[('parent_id', '=', False)])
    account_id = fields.Many2one(
        'account.account', string='Account',
        domain=[('deprecated', '=', False)], required=True)
    account_reconcile = fields.Boolean(
        related='account_id.reconcile', readonly=True)
    reconcile = fields.Selection([
        ('unreconciled', 'Unreconciled or Partially Reconciled'),
        ('reconciled', 'Fully Reconciled'),
        # ('partial_reconciled', 'Partially Reconciled'),
        ], string='Reconciliation Filter')

    @api.onchange('partner_id')
    def partner_id_change(self):
        if self.partner_id:
            if self.partner_id.customer:
                self.account_id =\
                    self.partner_id.property_account_receivable_id.id
            else:
                self.account_id =\
                    self.partner_id.property_account_payable_id.id

    def go(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account', 'action_account_moves_all_a')
        action['context'] = {'search_default_account_id': [self.account_id.id]}
        if self.partner_id:
            action['context']['search_default_partner_id'] =\
                [self.partner_id.id]
        if self.reconcile:
            action['context']['search_default_%s' % self.reconcile] = True
        return action
