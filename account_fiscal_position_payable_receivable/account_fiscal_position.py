# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    receivable_account_id = fields.Many2one(
        'account.account', string='Partner Receivable Account',
        company_dependent=True, domain=[('type', '=', 'receivable')])
    payable_account_id = fields.Many2one(
        'account.account', string='Partner Payable Account',
        company_dependent=True, domain=[('type', '=', 'payable')])


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('property_account_position')
    def fiscal_position_receivable_payable_change(self):
        fp = self.property_account_position
        ipo = self.env['ir.property']
        if fp.receivable_account_id:
            self.property_account_receivable = fp.receivable_account_id
        else:
            self.property_account_receivable = ipo.get(
                'property_account_receivable', 'res.partner')
        if fp.payable_account_id:
            self.property_account_payable = fp.payable_account_id
        else:
            self.property_account_payable = ipo.get(
                'property_account_payable', 'res.partner')
