# Copyright 2018-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    number = fields.Char(string="Number", readonly=True)

    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        select_str += ", ai.number"
        return select_str

    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += ", sub.number"
        return select_str

    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += ", ai.number"
        return group_by_str
