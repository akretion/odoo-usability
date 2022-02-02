# Copyright 2020 Akretion
# @author: Renato Lima <renato.lima@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo.tools import mute_logger
from odoo.tests.common import TransactionCase


class TestPartner(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner_values = {
            'name': 'Akretion Test Partner',
            'ref': '220',
        }
        self.partner = self._create_partner(self.partner_values)

    def _create_partner(self, values):
        return self.env['res.partner'].create(values)

    def test_partners_same_ref(self):
        """Check create two partners with same ref"""
        with self.assertRaises(IntegrityError), mute_logger('odoo.sql_db'):
            self._create_partner(self.partner_values)

    def test_partner_get_name(self):
        """Check partner name get"""
        self.assertEqual(
            self.partner._get_name(), '[220] Akretion Test Partner'
        )
