# -*- coding: utf-8 -*-
# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    receivable_account_id = fields.Many2one(
        'account.account', string='Partner Receivable Account',
        company_dependent=True, domain=[('internal_type', '=', 'receivable')])
    payable_account_id = fields.Many2one(
        'account.account', string='Partner Payable Account',
        company_dependent=True, domain=[('internal_type', '=', 'payable')])


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('property_account_position_id')
    def fiscal_position_receivable_payable_change(self):
        fp = self.property_account_position_id
        ipo = self.env['ir.property']
        if fp.receivable_account_id:
            self.property_account_receivable_id = fp.receivable_account_id
        else:
            self.property_account_receivable_id = ipo.get(
                'property_account_receivable_id', 'res.partner')
        if fp.payable_account_id:
            self.property_account_payable_id = fp.payable_account_id
        else:
            self.property_account_payable_id = ipo.get(
                'property_account_payable_id', 'res.partner')
