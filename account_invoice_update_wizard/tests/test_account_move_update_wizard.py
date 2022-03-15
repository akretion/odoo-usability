# Copyright 2018-2022 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestAccountInvoiceUpdateWizard(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer12 = cls.env.ref('base.res_partner_12')
        cls.product16 = cls.env.ref('product.product_product_16')
        uom_unit = cls.env.ref('uom.product_uom_categ_unit')

        cls.move1 = cls.env['account.move'].create({
            'name': 'Test invoice',
            'partner_id': cls.customer12.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                [0, None, {
                    'name': 'Line1',
                    'product_id': cls.product16.id,
                    'product_uom_id': uom_unit.id,
                    'quantity': 1,
                    'price_unit': 42.0,
                    'credit': 42.0,
                    'debit': 0
                }],
            ],
        })

        cls.aa1 = cls.env.ref('analytic.analytic_partners_camp_to_camp')
        cls.aa2 = cls.env.ref('analytic.analytic_nebula')
        cls.atag1 = cls.env.ref('analytic.tag_contract')
        cls.atag2 = cls.env['account.analytic.tag'].create({
            'name': 'の',
        })

    def create_wizard(self, move):
        res = move.prepare_update_wizard()
        self.wiz = self.env['account.move.update'].browse(res['res_id'])

    def test_add_analytic_account_line1(self):
        """ Add analytic account on a move line
        after the move has been approved.

        This will:
            - update the move line
            - create a new analytic line.
        """
        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_account_id = self.aa1
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_account_id, self.aa1)
        self.assertEqual(related_ml.analytic_line_ids.account_id, self.aa1)

    def test_change_analytic_account_line1(self):
        """ Change analytic account on a move line
        after the move has been approved.

        This will:
            - update the move line
            - update the existing analytic line."""
        move_line1 = self.move1.invoice_line_ids.filtered(lambda rec: rec.product_id == self.product16)
        move_line1.analytic_account_id = self.aa2

        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_account_id = self.aa1
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_account_id, self.aa1)
        self.assertEqual(related_ml.analytic_line_ids.account_id, self.aa1)

    def test_add_analytic_tags_line1(self):
        """ Add analytic tags on a move line
        after the move has been approved.

        This will update move line.
        """
        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_tag_ids = self.atag2
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_tag_ids, self.atag2)
        self.assertFalse(related_ml.analytic_line_ids)

    def test_change_analytic_tags_line1(self):
        """ Change analytic tags on a move line
        after the move has been approved.

        It will update move line and analytic line
        """
        move_line1 = self.move1.invoice_line_ids.filtered(lambda rec: rec.product_id == self.product16)
        move_line1.analytic_account_id = self.aa2
        move_line1.analytic_tag_ids = self.atag1

        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_tag_ids = self.atag2
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_tag_ids, self.atag2)
        self.assertEqual(related_ml.analytic_line_ids.tag_ids, self.atag2)

    def test_add_analytic_info_line1(self):
        """ Add analytic account and tags on a move line
        after the move has been approved.

        This will:
            - update move line
            - create an analytic line
        """
        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_account_id = self.aa1
        wiz_line.analytic_tag_ids = self.atag2
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_account_id, self.aa1)
        self.assertEqual(related_ml.analytic_tag_ids, self.atag2)
        self.assertEqual(related_ml.analytic_line_ids.account_id, self.aa1)
        self.assertEqual(related_ml.analytic_line_ids.tag_ids, self.atag2)

    def test_empty_analytic_account_line1(self):
        """ Remove analytic account
        after the move has been approved.

        This will raise an error as it is not implemented.
        """
        move_line1 = self.move1.invoice_line_ids.filtered(lambda rec: rec.product_id == self.product16)
        move_line1.analytic_account_id = self.aa2

        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_account_id = False
        self.wiz.run()
        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertFalse(related_ml.analytic_account_id)
        self.assertFalse(related_ml.analytic_line_ids)
