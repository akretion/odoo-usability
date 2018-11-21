# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin = fields.Float(string='Margin', readonly=True)

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += ", SUM(l.margin_company_currency) AS margin"
        return select_str
