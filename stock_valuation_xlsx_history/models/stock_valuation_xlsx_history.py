# Copyright 2026 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class StockValuationXlsxHistory(models.Model):
    _name = "stock.valuation.xlsx.history"
    _description = "Stock XLSX Export History"
    _order = "generated_at desc, id desc"
    _check_company_auto = True

    name = fields.Char(string="Filename", required=True, readonly=True)
    export_file = fields.Binary(
        string="XLSX Report", attachment=True, required=True, readonly=True
    )
    export_id = fields.Many2one(
        "stock.valuation.xlsx.export",
        string="Configuration",
        ondelete="set null",
        check_company=True,
        readonly=True,
    )
    company_id = fields.Many2one("res.company", required=True, readonly=True)
    report_type = fields.Selection(
        [("valuation", "Valuation"), ("variation", "Variation")],
        required=True,
        readonly=True,
    )
    location_id = fields.Many2one(
        "stock.location", check_company=True, readonly=True, ondelete="restrict"
    )
    generated_at = fields.Datetime(required=True, readonly=True)
    start_date = fields.Datetime(readonly=True)
    end_date = fields.Datetime(
        string="Valuation / End Date", required=True, readonly=True
    )
    parameters = fields.Json(string="Export Parameters", readonly=True)

    def action_download(self):
        self.ensure_one()
        self.check_access("read")
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{self._name}/{self.id}/export_file"
            "?download=true&filename_field=name",
            "target": "download",
        }
