# Copyright 2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    fiscal_classification_id = fields.Many2one(
        "account.product.fiscal.classification",
        string="Product Fiscal Classification",
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["fiscal_classification_id"] = "t.fiscal_classification_id"
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ", t.fiscal_classification_id"
        return res
