# -*- coding: utf-8 -*-
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestAccountInvoiceUpdateWizard(TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceUpdateWizard, self).setUp()
        self.customer12 = self.env.ref('base.res_partner_12')
        self.product16 = self.env.ref('product.product_product_16')
        self.product24 = self.env.ref('product.product_product_24')
        uom_unit = self.env.ref('product.product_uom_categ_unit')

        self.invoice1 = self.env['account.invoice'].create({
            'name': 'Test invoice',
            'partner_id': self.customer12.id,
        })
        self.inv_line1 = self.env['account.invoice.line'].create({
            'invoice_id': self.invoice1.id,
            'name': "Line1",
            'product_id': self.product16.id,
            'product_uom_id': uom_unit.id,
            'account_id': self.invoice1.account_id.id,
            'price_unit': 42.0,
        })
        self.inv_line2 = self.env['account.invoice.line'].create({
            'invoice_id': self.invoice1.id,
            'name': "Line2",
            'product_id': self.product24.id,
            'product_uom_id': uom_unit.id,
            'account_id': self.invoice1.account_id.id,
            'price_unit': 1111.1,
        })

        self.aa1 = self.env.ref('analytic.analytic_partners_camp_to_camp')
        self.aa2 = self.env.ref('analytic.analytic_nebula')
        self.atag1 = self.env.ref('analytic.tag_contract')
        self.atag2 = self.env['account.analytic.tag'].create({
            'name': u'の',
        })

    def create_wizard(self):
        UpdateWizard = self.env['account.invoice.update'].with_context(
            active_model='account.invoice',
            active_id=self.invoice1.id)
        self.wiz = UpdateWizard.create({})

    def test_add_analytic_account_line1(self):
        """ Add analytic account on an invoice line
        after the invoice has been approved.

        This will:
            - update the move line
            - create a new analytic line.
        """
        self.invoice1.action_invoice_open()
        self.create_wizard()

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id == self.inv_line1)
        wiz_line.account_analytic_id = self.aa1
        self.wiz.run()

        related_ml = self.invoice1.move_id.line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_account_id, self.aa1)
        self.assertEqual(related_ml.analytic_line_ids.account_id, self.aa1)

    def test_change_analytic_account_line1(self):
        """ Change analytic account on an invoice line
        after the invoice has been approved.

        This will:
            - update the move line
            - update the existing analytic line."""
        self.inv_line1.account_analytic_id = self.aa2

        self.invoice1.action_invoice_open()
        self.create_wizard()

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id == self.inv_line1)
        wiz_line.account_analytic_id = self.aa1
        self.wiz.run()

        related_ml = self.invoice1.move_id.line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_account_id, self.aa1)
        self.assertEqual(related_ml.analytic_line_ids.account_id, self.aa1)

    def test_error_grouped_move_lines(self):
        """ Change analytic account on an invoice line
        after the invoice has been approved where both
        lines were grouped in the same move line.

        This will raise an error.
        """
        self.invoice1.journal_id.group_invoice_lines = True

        self.inv_line2.product_id = self.product16
        self.inv_line2.unit_price = 42.0

        self.invoice1.action_invoice_open()
        self.create_wizard()

        line1 = self.wiz.line_ids[0]
        line1.account_analytic_id = self.aa1
        with self.assertRaises(UserError):
            self.wiz.run()

    def test_add_analytic_tags_line1(self):
        """ Add analytic tags on an invoice line
        after the invoice has been approved.

        This will update move line.
        """
        self.invoice1.action_invoice_open()
        self.create_wizard()

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id == self.inv_line1)
        wiz_line.analytic_tag_ids = self.atag2
        self.wiz.run()

        related_ml = self.invoice1.move_id.line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_tag_ids, self.atag2)
        self.assertFalse(related_ml.analytic_line_ids)

    def test_change_analytic_tags_line1(self):
        """ Change analytic tags on an invoice line
        after the invoice has been approved.

        It will update move line and analytic line
        """
        self.inv_line1.account_analytic_id = self.aa2
        self.inv_line1.analytic_tag_ids = self.atag1

        self.invoice1.action_invoice_open()
        self.create_wizard()

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id == self.inv_line1)
        wiz_line.analytic_tag_ids = self.atag2
        self.wiz.run()

        related_ml = self.invoice1.move_id.line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_tag_ids, self.atag2)
        self.assertEqual(related_ml.analytic_line_ids.tag_ids, self.atag2)

    def test_add_analytic_info_line1(self):
        """ Add analytic account and tags on an invoice line
        after the invoice has been approved.

        This will:
            - update move line
            - create an analytic line
        """
        self.invoice1.action_invoice_open()
        self.create_wizard()

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id == self.inv_line1)
        wiz_line.account_analytic_id = self.aa1
        wiz_line.analytic_tag_ids = self.atag2
        self.wiz.run()

        related_ml = self.invoice1.move_id.line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_account_id, self.aa1)
        self.assertEqual(related_ml.analytic_tag_ids, self.atag2)
        self.assertEqual(related_ml.analytic_line_ids.account_id, self.aa1)
        self.assertEqual(related_ml.analytic_line_ids.tag_ids, self.atag2)

    def test_empty_analytic_account_line1(self):
        """ Remove analytic account
        after the invoice has been approved.

        This will raise an error as it is not implemented.
        """
        self.inv_line1.account_analytic_id = self.aa2

        self.invoice1.action_invoice_open()
        self.create_wizard()

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id == self.inv_line1)
        wiz_line.account_analytic_id = False
        self.wiz.run()
        related_ml = self.invoice1.move_id.line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertFalse(related_ml.analytic_account_id)
        self.assertFalse(related_ml.analytic_line_ids)
