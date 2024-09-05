# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import SavepointCase


class TestProductDetailedType(SavepointCase):

    def test_product_detailed_type(self):
        p1 = self.env['product.product'].create({
            'name': 'Test 1',
            'detailed_type': 'service',
            })
        self.assertEqual(p1.type, 'service')
        p2 = self.env['product.product'].create({
            'name': 'Test 2',
            'detailed_type': 'consu',
            })
        self.assertEqual(p2.type, 'consu')

    def test_product_type_compat(self):
        p1 = self.env['product.product'].create({
            'name': 'Test 1',
            'type': 'service',
            })
        self.assertEqual(p1.type, 'service')
        self.assertEqual(p1.detailed_type, 'service')
        p2 = self.env['product.product'].create({
            'name': 'Test 1',
            'type': 'consu',
            })
        self.assertEqual(p2.type, 'consu')
        self.assertEqual(p2.detailed_type, 'consu')
