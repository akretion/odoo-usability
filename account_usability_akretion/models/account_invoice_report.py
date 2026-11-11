# Copyright 2022-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    industry_id = fields.Many2one('res.partner.industry', string='Partner Industry', readonly=True)

    def _select_list(self, table):
        res = super()._select_list(table)
        res.append(table.partner_id.industry_id)
        return res
