# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    account_id = fields.Many2one(
        'account.account',
        compute="_compute_account_id", store=True, readonly=False, check_company=True,
        domain="[('company_id', '=', company_id), ('deprecated', '=', False)]")
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account',
        domain="[('company_id', 'in', [False, company_id])]",
        check_company=True)

    @api.depends('move_line_id', 'partner_id')
    def _compute_account_id(self):
        for line in self:
            account_id = False
            if not line.move_line_id and line.partner_id:
                partner = line.partner_id.with_company(line.order_id.company_id.id)
                if line.order_id.payment_type == "inbound":
                    account_id = partner.property_account_receivable_id.id
                else:
                    account_id = partner.property_account_payable_id.id
            line.account_id = account_id

    # take info account account_id for grouping
    def payment_line_hashcode(self):
        hashcode = super().payment_line_hashcode()
        account_str = str(self.account_id.id or False)
        analytic_account_str = str(self.analytic_account_id.id or False)
        hashcode = '-'.join([hashcode, account_str, analytic_account_str])
        return hashcode
