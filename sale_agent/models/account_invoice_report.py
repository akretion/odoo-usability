# Copyright 2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import SQL


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    invoice_agent_id = fields.Many2one("res.partner", string="Agent", readonly=True)

    def _select(self):
        return SQL("%s, move.invoice_agent_id AS invoice_agent_id", super()._select())
