# Copyright 2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    industry_id = fields.Many2one('res.partner.industry', string='Partner Industry', readonly=True)

    @api.model
    def _select(self):
        res = super()._select()
        res += ", COALESCE(partner.industry_id, commercial_partner.industry_id) AS industry_id"
        return res
