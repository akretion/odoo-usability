# Copyright 2018-2022 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command, fields
from odoo.tests.common import TransactionCase


class TestAccountInvoiceUpdateWizard(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.customer12 = cls.env.ref('base.res_partner_12')
        cls.product16 = cls.env.ref('product.product_product_16')
        uom_unit = cls.env.ref('uom.product_uom_categ_unit')

        cls.term_30 = cls.env['account.payment.term'].create({
            'name': '30 days',
            'line_ids': [Command.create({'nb_days': 30})],
        })
        cls.term_60 = cls.env['account.payment.term'].create({
            'name': '60 days',
            'line_ids': [Command.create({'nb_days': 60})],
        })

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

    def test_update_account_on_posted_invoice(self):
        """Change the account of a line of a posted invoice."""
        self.move1.action_post()
        line = self.move1.invoice_line_ids
        other_account = self.env['account.account'].search([
            ('company_ids', 'in', self.env.company.id),
            ('deprecated', '=', False),
            ('account_type', 'not in', (
                'asset_receivable', 'liability_payable', 'off_balance')),
            ('id', '!=', line.account_id.id),
        ], limit=1)
        self.assertTrue(other_account)
        self.create_wizard(self.move1)
        wiz_line = self.wiz.line_ids
        self.assertEqual(wiz_line.account_id, line.account_id)
        wiz_line.account_id = other_account
        self.wiz.run()
        self.assertEqual(line.account_id, other_account)

    def test_update_due_date_without_payment_term(self):
        """Without a payment term, the due date is editable and drives the
        maturity date of the payment term line."""
        self.move1.write({
            'invoice_date': fields.Date.today(),
            'invoice_payment_term_id': False,
        })
        self.move1.action_post()
        new_due = fields.Date.add(self.move1.invoice_date, days=45)
        self.create_wizard(self.move1)
        self.assertEqual(self.wiz.invoice_date_due, self.move1.invoice_date_due)
        self.wiz.invoice_date_due = new_due
        self.wiz.run()
        self.assertEqual(self.move1.invoice_date_due, new_due)
        term_line = self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')
        self.assertEqual(len(term_line), 1)
        self.assertEqual(term_line.date_maturity, new_due)

    def test_update_payment_term(self):
        """Changing the payment term recomputes the due date and moves the
        maturity date of the payment term line."""
        self.move1.write({
            'invoice_date': fields.Date.today(),
            'invoice_payment_term_id': self.term_30.id,
        })
        self.move1.action_post()
        self.create_wizard(self.move1)
        self.wiz.invoice_payment_term_id = self.term_60
        self.wiz.run()
        new_due = fields.Date.add(self.move1.invoice_date, days=60)
        self.assertEqual(self.move1.invoice_payment_term_id, self.term_60)
        self.assertEqual(self.move1.invoice_date_due, new_due)
        term_line = self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')
        self.assertEqual(len(term_line), 1)
        self.assertEqual(term_line.date_maturity, new_due)

    def test_due_date_ignored_with_payment_term(self):
        """When a payment term is set, the due date is computed from it: the
        one typed in the wizard is not used."""
        self.move1.write({
            'invoice_date': fields.Date.today(),
            'invoice_payment_term_id': self.term_30.id,
        })
        self.move1.action_post()
        expected = self.move1.invoice_date_due
        self.create_wizard(self.move1)
        self.wiz.invoice_date_due = fields.Date.add(expected, days=10)
        self.wiz.run()
        self.assertEqual(self.move1.invoice_date_due, expected)

    def _sale_invoice_with_term(self, term):
        self.move1.write({
            'invoice_date': fields.Date.today(),
            'invoice_payment_term_id': term.id,
        })
        self.move1.action_post()
        return self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')

    def _two_line_term(self, name, first, second):
        return self.env['account.payment.term'].create({
            'name': name,
            'line_ids': [
                Command.create({
                    'value': 'percent',
                    'value_amount': first,
                    'nb_days': 30,
                }),
                Command.create({
                    'value': 'percent',
                    'value_amount': second,
                    'nb_days': 60,
                }),
            ],
        })

    def test_payment_term_update_keeps_the_manual_label(self):
        """The label of a payment term line set by hand is kept when the
        payment term is changed."""
        self._sale_invoice_with_term(self.term_30)
        term_line = self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')
        term_line.name = 'Acompte client'
        self.create_wizard(self.move1)
        self.wiz.invoice_payment_term_id = self.term_60
        self.wiz.run()
        self.assertEqual(term_line.name, 'Acompte client')
        self.assertEqual(
            term_line.date_maturity,
            fields.Date.add(self.move1.invoice_date, days=60))

    def test_switch_from_two_terms_to_one_merges_the_instalments(self):
        """Switching to a single term deletes the surplus payment term line
        of the posted move (same total, new split of the receivable)."""
        term_50_50 = self._two_line_term('50/50', 50.0, 50.0)
        term_lines = self._sale_invoice_with_term(term_50_50)
        self.assertEqual(len(term_lines), 2)
        total = self.move1.amount_total
        self.create_wizard(self.move1)
        self.wiz.invoice_payment_term_id = self.term_30
        self.wiz.run()
        term_lines = self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')
        self.assertEqual(len(term_lines), 1)
        self.assertAlmostEqual(term_lines.balance, total, places=2)
        self.assertEqual(
            term_lines.date_maturity,
            fields.Date.add(self.move1.invoice_date, days=30))
        self.assertEqual(self.move1.invoice_payment_term_id, self.term_30)
        # the move is still balanced, with the same total and residual
        self.assertAlmostEqual(
            sum(self.move1.line_ids.mapped('balance')), 0.0, places=2)
        self.assertAlmostEqual(self.move1.amount_total, total, places=2)
        self.assertAlmostEqual(self.move1.amount_residual, total, places=2)

    def test_switch_from_one_term_to_two_terms_splits_it(self):
        self._sale_invoice_with_term(self.term_30)
        total = self.move1.amount_total
        self.create_wizard(self.move1)
        self.wiz.invoice_payment_term_id = self._two_line_term(
            '50/50', 50.0, 50.0)
        self.wiz.run()
        term_lines = self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')
        self.assertEqual(len(term_lines), 2)
        self.assertAlmostEqual(
            sum(term_lines.mapped('balance')), total, places=2)
        self.assertEqual(
            sorted(term_lines.mapped('date_maturity')),
            sorted([
                fields.Date.add(self.move1.invoice_date, days=30),
                fields.Date.add(self.move1.invoice_date, days=60),
            ]))
        self.assertAlmostEqual(
            sum(self.move1.line_ids.mapped('balance')), 0.0, places=2)

    def test_switch_to_another_amount_split(self):
        """The amounts of the payment term lines follow the new split."""
        term_50_50 = self._two_line_term('50/50', 50.0, 50.0)
        self._sale_invoice_with_term(term_50_50)
        total = self.move1.amount_total
        self.create_wizard(self.move1)
        self.wiz.invoice_payment_term_id = self._two_line_term(
            '40/60', 40.0, 60.0)
        self.wiz.run()
        balances = self.move1.line_ids.filtered(
            lambda x: x.display_type == 'payment_term').mapped('balance')
        self.assertAlmostEqual(sum(balances), total, places=2)
        self.assertAlmostEqual(
            sorted(balances)[0], round(total * 0.4, 2), places=2)
