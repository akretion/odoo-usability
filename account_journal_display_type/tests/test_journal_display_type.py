from odoo.tests import SavepointCase
from odoo.tests.common import new_test_user, users


class TestJournalDisplayType(SavepointCase):
    def setUp(self):
        super().setUp()

        self.account = self.env["account.account"].create(
            {
                "name": "Test account",
                "code": "TAC",
                "user_type_id": self.env.ref("account.data_account_type_payable").id,
                "reconcile": True,
            }
        )
        self.manager = new_test_user(
            self.env, "test_manager", "account.group_account_manager"
        )

    @users("test_manager")
    def test_journal_payment_with_account(self):

        journal = self.env["account.journal"].create(
            {
                "name": "Bank with account",
                "display_type": "cash",
                "type": "cash",
                "code": "BK100",
                "payment_debit_account_id": self.account.id,
                "payment_credit_account_id": self.account.id,
            }
        )
        journal.display_type = "payment"
        self.assertEqual(journal.type, "bank")
        self.assertEqual(journal.default_account_id, journal.payment_debit_account_id)

    @users("test_manager")
    def test_journal_payment_without_account(self):

        journal = self.env["account.journal"].create(
            {
                "name": "Bank without account",
                "display_type": "payment",
                "type": "bank",
                "code": "BK101",
            }
        )
        self.assertTrue(journal.payment_debit_account_id)
        self.assertTrue(journal.payment_credit_account_id)
        self.assertEqual(journal.type, "bank")
        self.assertEqual(journal.default_account_id, journal.payment_debit_account_id)

    @users("test_manager")
    def test_journal_cash_with_account(self):

        journal = self.env["account.journal"].create(
            {
                "name": "Cash with account",
                "display_type": "cash",
                "type": "cash",
                "code": "BK102",
                "default_account_id": self.account.id,
            }
        )
        self.assertEqual(journal.type, "cash")
        self.assertEqual(journal.default_account_id, self.account)
        self.assertEqual(journal.default_account_id, journal.payment_debit_account_id)
        self.assertEqual(journal.default_account_id, journal.payment_credit_account_id)

    @users("test_manager")
    def test_journal_bank_without_account(self):

        journal = self.env["account.journal"].create(
            {
                "name": "Bank without account",
                "type": "bank",
                "code": "BK103",
            }
        )
        self.assertTrue(journal.payment_debit_account_id)
