# Copyright 2026 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
from datetime import timedelta
from io import BytesIO
from unittest.mock import Mock, patch
from zipfile import ZipFile

from odoo import fields
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestStockValuationXlsxHistory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Export = cls.env["stock.valuation.xlsx.export"]
        cls.History = cls.env["stock.valuation.xlsx.history"]
        cls.category = cls.env["product.category"].create({"name": "History Test"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "History Test Product",
                "is_storable": True,
                "categ_id": cls.category.id,
                "standard_price": 12,
            }
        )
        cls.valuation = cls.Export.create(
            {
                "name": "Daily Valuation",
                "categ_ids": [fields.Command.set(cls.category.ids)],
            }
        )
        cls.variation = cls.Export.create(
            {
                "name": "Rolling Variation",
                "report_type": "variation",
                "categ_ids": [fields.Command.set(cls.category.ids)],
            }
        )
        cls.env["stock.quant"]._update_available_quantity(
            cls.product,
            cls.valuation.warehouse_id.lot_stock_id
            or cls.env["stock.warehouse"]
            .search([("company_id", "=", cls.env.company.id)], limit=1)
            .lot_stock_id,
            5,
        )
        cls.reader = new_test_user(
            cls.env,
            login="stock_history_reader",
            groups="stock.group_stock_user",
            company_id=cls.env.company.id,
            company_ids=[fields.Command.set(cls.env.company.ids)],
        )
        cls.manager = new_test_user(
            cls.env,
            login="stock_history_manager",
            groups="stock.group_stock_manager",
            company_id=cls.env.company.id,
            company_ids=[fields.Command.set(cls.env.company.ids)],
        )

    def _assert_workbook(self, history):
        self.assertTrue(history.name.endswith(".xlsx"))
        with ZipFile(BytesIO(base64.b64decode(history.export_file))) as workbook:
            self.assertIsNone(workbook.testzip())
            self.assertIn("xl/worksheets/sheet1.xml", workbook.namelist())
            self.assertIn(
                b"History Test Product", workbook.read("xl/sharedStrings.xml")
            )

    def test_crons_generate_only_their_active_configurations(self):
        self.valuation.copy({"active": False})
        valuation_cron = self.env.ref(
            "stock_valuation_xlsx_history.ir_cron_stock_valuation_xlsx"
        )
        variation_cron = self.env.ref(
            "stock_valuation_xlsx_history.ir_cron_stock_variation_xlsx"
        )
        valuation_cron.ir_actions_server_id.run()
        history = self.History.search([])
        self.assertEqual(history.export_id, self.valuation)
        self._assert_workbook(history)
        variation_cron.ir_actions_server_id.run()
        history = self.History.search([("export_id", "=", self.variation.id)])
        self.assertEqual(len(history), 1)
        self._assert_workbook(history)
        self.assertEqual(self.History.search_count([]), 2)
        valuation_cron.ir_actions_server_id.run()
        self.assertEqual(self.History.search_count([]), 3)

    def test_attachment_survives_wizard_and_configuration_removal(self):
        history = self.valuation.with_user(self.manager)._generate_export()
        original = history.export_file
        self.env["stock.valuation.xlsx"].search([]).unlink()
        self.valuation.unlink()
        history.invalidate_recordset()
        self.assertFalse(history.export_id)
        self.assertEqual(history.export_file, original)
        attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", history._name),
                ("res_id", "=", history.id),
                ("res_field", "=", "export_file"),
            ]
        )
        self.assertEqual(len(attachment), 1)
        self.assertFalse(attachment.public)
        history = history.with_user(self.reader)
        action = history.action_download()
        self.assertIn(f"/{history.id}/export_file?download=true", action["url"])
        binary = history.env["ir.binary"]
        record = binary._find_record(
            res_model=history._name, res_id=history.id, field="export_file"
        )
        with patch(
            "odoo.addons.base.models.ir_attachment.request",
            Mock(db=self.cr.dbname),
        ):
            stream = binary._get_stream_from(
                record, "export_file", filename_field="name"
            )
        self.assertEqual(stream.download_name, history.name)
        self.assertGreater(stream.size, 0)

    def test_relative_dates_advance_and_fixed_dates_stay(self):
        now = fields.Datetime.now()
        self.valuation.write({"stock_date_type": "past", "valuation_days_ago": 7})
        first = self.valuation._prepare_wizard_values(now)
        next_run = self.valuation._prepare_wizard_values(now + timedelta(days=1))
        self.assertEqual(
            fields.Datetime.to_datetime(first["past_date"]), now - timedelta(days=7)
        )
        self.assertEqual(
            fields.Datetime.to_datetime(next_run["past_date"]), now - timedelta(days=6)
        )
        self.variation.write({"end_date_type": "past", "end_days_ago": 2})
        values = self.variation._prepare_wizard_values(now)
        self.assertEqual(
            fields.Datetime.to_datetime(values["start_date"]), now - timedelta(days=30)
        )
        self.assertEqual(
            fields.Datetime.to_datetime(values["end_date"]), now - timedelta(days=2)
        )
        self.variation.write(
            {
                "date_mode": "fixed",
                "start_date": now - timedelta(days=10),
                "end_date": now - timedelta(days=1),
            }
        )
        self.assertEqual(
            self.variation._prepare_wizard_values(now),
            self.variation._prepare_wizard_values(now + timedelta(days=1)),
        )

    def test_invalid_dates_are_rejected(self):
        cases = [
            (self.valuation, {"stock_date_type": "past", "valuation_days_ago": -1}),
            (self.valuation, {"stock_date_type": "past", "date_mode": "fixed"}),
            (self.variation, {"start_days_ago": 0}),
            (self.variation, {"end_date_type": "past", "end_days_ago": 30}),
            (self.variation, {"end_date_type": "past", "end_days_ago": -1}),
            (
                self.variation,
                {
                    "date_mode": "fixed",
                    "start_date": fields.Datetime.now() + timedelta(days=1),
                },
            ),
        ]
        for config, values in cases:
            with (
                self.subTest(values=values),
                self.assertRaises(ValidationError),
                self.cr.savepoint(),
            ):
                config.write(values)

    def test_past_exports_and_parameter_snapshot(self):
        self.valuation.write(
            {
                "stock_date_type": "past",
                "valuation_days_ago": 2,
                "categ_subtotal": False,
                "split_by_lot": True,
                "split_by_location": True,
                "apply_depreciation": False,
            }
        )
        history = self.valuation._generate_export()
        self.assertEqual(history.parameters["categ_ids"][0][2], self.category.ids)
        self.assertFalse(history.parameters["categ_subtotal"])
        self.assertTrue(history.parameters["split_by_lot"])
        self.assertFalse(history.parameters["apply_depreciation"])
        self.assertEqual(history.end_date, history.generated_at - timedelta(days=2))
        self.valuation.categ_subtotal = True
        self.assertFalse(history.parameters["categ_subtotal"])
        self.variation.write({"end_date_type": "past", "end_days_ago": 1})
        history = self.variation._generate_export()
        self.assertEqual(history.end_date, history.generated_at - timedelta(days=1))

    def test_other_company_is_isolated_in_generation_and_download(self):
        company = self.env["res.company"].create({"name": "Other History Company"})
        config = self.Export.create(
            {
                "name": "Other Company",
                "company_id": company.id,
                "categ_ids": [fields.Command.set(self.category.ids)],
            }
        )
        captured = []
        original_generate = type(self.env["stock.valuation.xlsx"]).generate

        def capture_generate(wizard):
            captured.append((wizard.env.company, wizard.env.companies))
            return original_generate(wizard)

        with patch.object(
            type(self.env["stock.valuation.xlsx"]), "generate", capture_generate
        ):
            history = config._generate_export()
        self.assertEqual(captured, [(company, company)])
        self.assertEqual(history.company_id, company)
        reader_history = history.with_user(self.reader).with_context(
            allowed_company_ids=self.reader.company_ids.ids
        )
        self.assertFalse(reader_history.search([("id", "=", history.id)]))
        with self.assertRaises(AccessError):
            reader_history.action_download()
        with self.assertRaises(AccessError):
            reader_history.env["ir.binary"]._find_record(
                res_model=history._name, res_id=history.id, field="export_file"
            )
        with self.assertRaises(UserError), self.cr.savepoint():
            config.location_id = self.valuation.location_id

    def test_reader_cannot_generate_or_modify_history(self):
        history = self.valuation._generate_export().with_user(self.reader)
        with self.assertRaises(AccessError):
            self.valuation.with_user(self.reader).action_generate()
        with self.assertRaises(AccessError):
            history.write({"name": "changed.xlsx"})
        with self.assertRaises(AccessError):
            history.unlink()

    def test_failed_generation_creates_no_history(self):
        with patch.object(
            type(self.env["stock.valuation.xlsx"]),
            "generate",
            side_effect=UserError("Export failed"),
        ):
            with self.assertRaises(UserError), self.cr.savepoint():
                self.Export._cron_generate_valuation()
        self.assertFalse(self.History.search([]))

    def test_empty_generation_creates_no_history(self):
        with patch.object(
            type(self.env["stock.valuation.xlsx"]), "generate", return_value=None
        ):
            with self.assertRaises(ValidationError), self.cr.savepoint():
                self.valuation._generate_export()
        self.assertFalse(self.History.search([]))
