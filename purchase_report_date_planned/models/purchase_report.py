from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    date_planned = fields.Datetime(store=True)

    def _select(self):
        select_str = super(PurchaseReport, self)._select()
        return select_str + ", l.date_planned as date_planned"

    def _group_by(self):
        group_by_str = super(PurchaseReport, self)._group_by()
        return group_by_str + ", l.date_planned"
