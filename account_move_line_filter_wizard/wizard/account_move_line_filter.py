# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveLineFilterWizard(models.TransientModel):
    _name = 'account.move.line.filter.wizard'
    _description = 'Wizard for easy and fast access to account move lines'

    date_range_id = fields.Many2one(
        'date.range', string='Date Range (only for General Ledger)')
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

    @api.model
    def default_get(self, fields_list):
        res = super(AccountMoveLineFilterWizard, self).default_get(fields_list)
        today = fields.Date.context_today(self)
        fy_type_id = self.env.ref('account_fiscal_year.fiscalyear').id
        dro = self.env['date.range']
        date_range = dro.search([
            ('type_id', '=', fy_type_id),
            ('company_id', '=', self.env.user.company_id.id),
            ('date_start', '<=', today),
            ('date_end', '>=', today)
            ], limit=1)
        if not date_range:
            date_range = dro.search([
                ('type_id', '=', fy_type_id),
                ('company_id', '=', self.env.user.company_id.id),
                ], order='date_start desc', limit=1)
        if date_range:
            res['date_range_id'] = date_range.id
        return res

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

    def show_report_general_ledger(self):
        self.ensure_one()
        if self.account_reconcile:
            assert self.reconcile != 'unreconciled'
        if not self.date_range_id:
            raise UserError(_(
                "Select a date range to show the General Ledger report."))
        wvals = {
            'account_ids': [(6, 0, [self.account_id.id])],
            'date_from': self.date_range_id.date_start,
            'date_to': self.date_range_id.date_end,
            }
        if self.partner_id:
            wvals['partner_ids'] = [(6, 0, [self.partner_id.id])]
        wiz = self.env['general.ledger.report.wizard'].create(wvals)
        action = wiz.button_export_html()
        return action

    def show_report_open_items(self):
        self.ensure_one()
        assert self.account_reconcile and self.reconcile == 'unreconciled'
        wvals = {
            'account_ids': [(6, 0, [self.account_id.id])],
            }
        if self.partner_id:
            wvals['partner_ids'] = [(6, 0, [self.partner_id.id])]
        wiz = self.env['open.items.report.wizard'].create(wvals)
        action = wiz.button_export_html()
        return action
