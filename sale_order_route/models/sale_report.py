# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    route_id = fields.Many2one('stock.location.route', string='Route', readonly=True)

    def _select_additional_fields(self, fields):
        fields['route_id'] = ", s.route_id AS route_id"
        return super()._select_additional_fields(fields)

    def _group_by_sale(self, groupby=''):
        res = super()._group_by_sale(groupby=groupby)
        res += ', s.route_id'
        return res
