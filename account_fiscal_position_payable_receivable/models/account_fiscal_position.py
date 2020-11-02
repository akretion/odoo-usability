# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    receivable_account_id = fields.Many2one(
        "account.account",
        string="Partner Receivable Account",
        company_dependent=True,
        domain=[("internal_type", "=", "receivable")],
    )
    payable_account_id = fields.Many2one(
        "account.account",
        string="Partner Payable Account",
        company_dependent=True,
        domain=[("internal_type", "=", "payable")],
    )
