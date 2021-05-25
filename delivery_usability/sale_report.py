# -*- coding: utf-8 -*-
# Copyright 2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    carrier_id = fields.Many2one(
        "delivery.carrier", string="Delivery Method", readonly=True)

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += ", s.carrier_id as carrier_id"
        return select_str

    def _group_by(self):
        groupby_str = super(SaleReport, self)._group_by()
        groupby_str += ", s.carrier_id"
        return groupby_str
