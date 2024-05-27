# Copyright 2018-2022 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestStockLocationSimple(TransactionCase):
    def setUp(self):
        super().setUp()
        self.env["stock.warehouse"].search([])._check_locations_created_by_warehouse()

    def test_location_checked_at_warehouse_creation(self):
        warehouse = self.env["stock.warehouse"].create({"name": "Test", "code": "TEST"})
        self.assertTrue(warehouse.view_location_id.is_created_by_warehouse)

    def test_native_location_checked(self):
        location_id = self.env.ref("stock.warehouse0").view_location_id

        self.assertTrue(location_id.is_created_by_warehouse)
