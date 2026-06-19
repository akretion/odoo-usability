# Copyright 2018-2022 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo import Command


class TestAccountInvoiceUpdateWizard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer12 = cls.env.ref('base.res_partner_12')
        cls.product16 = cls.env.ref('product.product_product_16')
        uom_unit = cls.env.ref('uom.product_uom_categ_unit')

        cls.plan = cls.env['account.analytic.plan'].create({'name': 'Test Plan'})
        cls.analytic_account_1 = cls.env['account.analytic.account'].create({
            'name': 'analytic 1 test plan',
            'plan_id': cls.plan.id,
            'company_id': False,
        })
        cls.analytic_account_2 = cls.env['account.analytic.account'].create({
            'name': 'analytic 2 test plan',
            'plan_id': cls.plan.id,
            'company_id': False,
        })
        cls.move1 = cls.env['account.move'].create({
            'name': 'Test invoice',
            'partner_id': cls.customer12.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': 'Line1',
                    'product_id': cls.product16.id,
                    'product_uom_id': uom_unit.id,
                    'quantity': 1,
                    'price_unit': 42.0,
                }),
            ],
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
        wiz_line.analytic_distribution = {self.analytic_account_1.id: 50, self.analytic_account_2.id: 50}
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_distribution, {str(self.analytic_account_1.id): 50.0, str(self.analytic_account_2.id): 50.0})
        self.assertEqual(len(related_ml.analytic_line_ids), 2)
        self.assertEqual(related_ml.analytic_line_ids[0].amount, 21.0)

    def test_change_analytic_account_line1(self):
        """ Change analytic account on a move line
        after the move has been approved.

        This will:
            - update the move line
            - update the existing analytic line."""
        move_line1 = self.move1.invoice_line_ids.filtered(lambda rec: rec.product_id == self.product16)
        move_line1.analytic_distribution = {self.analytic_account_1.id: 100}

        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_distribution = {self.analytic_account_1.id: 50, self.analytic_account_2.id: 50}
        self.wiz.run()

        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertEqual(related_ml.analytic_distribution, {str(self.analytic_account_1.id): 50.0, str(self.analytic_account_2.id): 50.0})
        self.assertEqual(len(related_ml.analytic_line_ids), 2)
        self.assertEqual(related_ml.analytic_line_ids[0].amount, 21.0)

    def test_empty_analytic_account_line1(self):
        """ Remove analytic account
        after the move has been approved.

        This will raise an error as it is not implemented.
        """
        move_line1 = self.move1.invoice_line_ids.filtered(lambda rec: rec.product_id == self.product16)
        move_line1.analytic_distribution = {self.analytic_account_1.id: 100}

        self.move1._post()
        self.create_wizard(self.move1)

        wiz_line = self.wiz.line_ids.filtered(
            lambda rec: rec.invoice_line_id.product_id.id == self.product16.id)
        wiz_line.analytic_distribution = False
        self.wiz.run()
        related_ml = self.move1.invoice_line_ids.filtered(
            lambda rec: rec.product_id == self.product16)
        self.assertFalse(related_ml.analytic_distribution)
        self.assertFalse(related_ml.analytic_line_ids)
