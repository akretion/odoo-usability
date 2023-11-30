# Copyright 2018-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin = fields.Float(string='Margin', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['margin_company_currency'] =\
            ", SUM(l.margin_company_currency) AS margin"
        res = super(SaleReport, self)._query(
            with_clause=with_clause, fields=fields, groupby=groupby,
            from_clause=from_clause)
        return res
