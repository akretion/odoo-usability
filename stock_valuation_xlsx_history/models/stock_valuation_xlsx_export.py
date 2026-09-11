# Copyright 2026 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockValuationXlsxExport(models.Model):
    _name = "stock.valuation.xlsx.export"
    _description = "Scheduled Stock XLSX Export Configuration"
    _check_company_auto = True

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    report_type = fields.Selection(
        [("valuation", "Valuation"), ("variation", "Variation")],
        required=True,
        default="valuation",
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        check_company=True,
        domain="[('company_id', '=', company_id)]",
    )
    location_id = fields.Many2one(
        "stock.location",
        string="Root Stock Location",
        required=True,
        check_company=True,
        compute="_compute_location_id",
        store=True,
        readonly=False,
        precompute=True,
        domain="[('usage', 'in', ('view', 'internal')), "
        "('company_id', 'in', [False, company_id])]",
    )
    categ_ids = fields.Many2many(
        "product.category",
        string="Product Category Filter",
        help="Leave empty to include all product categories and their children.",
    )
    categ_subtotal = fields.Boolean(string="Subtotals per Categories", default=True)
    date_mode = fields.Selection(
        [("relative", "Rolling Dates"), ("fixed", "Fixed Dates")],
        required=True,
        default="relative",
        help="Rolling dates are calculated at each execution, in 24-hour days before it.",
    )
    stock_date_type = fields.Selection(
        [("present", "Present"), ("past", "Past")],
        string="Valuation Temporality",
        required=True,
        default="present",
    )
    past_date = fields.Datetime(string="Valuation Date")
    valuation_days_ago = fields.Integer(default=1)
    standard_price_date = fields.Selection(
        [("past", "Past Date"), ("present", "Current")],
        string="Cost Price Date",
        required=True,
        default="past",
    )
    split_by_lot = fields.Boolean(string="Display Lots")
    split_by_location = fields.Boolean(string="Display Stock Locations")
    apply_depreciation = fields.Boolean(string="Apply Depreciation Rules", default=True)
    start_date = fields.Datetime()
    start_days_ago = fields.Integer(default=30)
    end_date_type = fields.Selection(
        [("present", "Present"), ("past", "Past")],
        string="End Date Temporality",
        required=True,
        default="present",
    )
    end_date = fields.Datetime()
    end_days_ago = fields.Integer(default=1)
    standard_price_start_date_type = fields.Selection(
        [("start", "Start Date"), ("present", "Current")],
        string="Cost Price for Start Date",
        required=True,
        default="start",
    )
    standard_price_end_date_type = fields.Selection(
        [("end", "End Date"), ("present", "Current")],
        string="Cost Price for End Date",
        required=True,
        default="end",
    )

    @api.depends("warehouse_id", "company_id")
    def _compute_location_id(self):
        for config in self:
            warehouse = config.warehouse_id or self.env["stock.warehouse"].search(
                [("company_id", "=", config.company_id.id)], limit=1
            )
            config.location_id = warehouse.view_location_id

    @api.constrains(
        "report_type",
        "date_mode",
        "stock_date_type",
        "past_date",
        "valuation_days_ago",
        "start_date",
        "start_days_ago",
        "end_date_type",
        "end_date",
        "end_days_ago",
    )
    def _check_dates(self):
        for config in self:
            config._prepare_wizard_values(fields.Datetime.now())

    def _prepare_wizard_values(self, now):
        self.ensure_one()
        values = {
            "company_id": self.company_id.id,
            "warehouse_id": self.warehouse_id.id,
            "location_id": self.location_id.id,
            "categ_ids": [fields.Command.set(self.categ_ids.ids)],
            "categ_subtotal": self.categ_subtotal,
        }
        if self.report_type == "valuation":
            past_date = False
            if self.stock_date_type == "past":
                if self.date_mode == "relative":
                    if self.valuation_days_ago < 0:
                        raise ValidationError(
                            _("Valuation days ago must be nonnegative.")
                        )
                    past_date = now - timedelta(days=self.valuation_days_ago)
                else:
                    past_date = self.past_date
                if not past_date or past_date > now:
                    raise ValidationError(_("Set a valuation date in the past."))
            values.update(
                stock_date_type=self.stock_date_type,
                past_date=fields.Datetime.to_string(past_date),
                standard_price_date=self.standard_price_date,
                split_by_lot=self.split_by_lot,
                split_by_location=self.split_by_location,
                apply_depreciation=self.apply_depreciation,
            )
        else:
            if self.date_mode == "relative":
                if self.start_days_ago <= 0 or (
                    self.end_date_type == "past" and self.end_days_ago < 0
                ):
                    raise ValidationError(
                        _("Use positive start days and nonnegative end days.")
                    )
                start_date = now - timedelta(days=self.start_days_ago)
                end_date = (
                    now - timedelta(days=self.end_days_ago)
                    if self.end_date_type == "past"
                    else now
                )
            else:
                start_date = self.start_date
                end_date = self.end_date if self.end_date_type == "past" else now
            if not start_date or not end_date or not start_date < end_date <= now:
                raise ValidationError(
                    _(
                        "The start date must precede the end date, which cannot be in the future."
                    )
                )
            values.update(
                start_date=fields.Datetime.to_string(start_date),
                end_date_type=self.end_date_type,
                end_date=fields.Datetime.to_string(end_date),
                standard_price_start_date_type=self.standard_price_start_date_type,
                standard_price_end_date_type=self.standard_price_end_date_type,
            )
        return values

    def _generate_export(self):
        self.ensure_one()
        self.check_access("write")
        config = self.with_company(self.company_id).with_context(
            allowed_company_ids=[self.company_id.id], bin_size=False
        )
        now = fields.Datetime.now()
        values = config._prepare_wizard_values(now)
        wizard = config.env[f"stock.{self.report_type}.xlsx"].create(values)
        wizard.generate()
        if not wizard.export_file or not wizard.export_filename:
            raise ValidationError(_("The export wizard did not produce an XLSX file."))
        return config.env["stock.valuation.xlsx.history"].create(
            {
                "name": wizard.export_filename,
                "export_file": wizard.export_file,
                "export_id": self.id,
                "company_id": self.company_id.id,
                "report_type": self.report_type,
                "location_id": self.location_id.id,
                "generated_at": now,
                "start_date": values.get("start_date"),
                "end_date": values.get("end_date") or values.get("past_date") or now,
                "parameters": values,
            }
        )

    def action_generate(self):
        self.ensure_one()
        return self._generate_export().action_download()

    @api.model
    def _cron_generate_valuation(self):
        for config in self.search([("report_type", "=", "valuation")]):
            config._generate_export()

    @api.model
    def _cron_generate_variation(self):
        for config in self.search([("report_type", "=", "variation")]):
            config._generate_export()
