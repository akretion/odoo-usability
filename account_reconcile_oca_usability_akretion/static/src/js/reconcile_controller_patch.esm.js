import {patch} from "@web/core/utils/patch";
import {ReconcileController} from "@account_reconcile_oca/js/reconcile/reconcile_controller.esm";

patch(ReconcileController.prototype, {

    /* Modify the behavior of the method updateJournalInfo() of the OCA module
       account_reconcile_oca to get the accounting balance instead of
       the balance from the bank statement */
    async updateJournalInfo() {
        var bank_journal_id = this.journalId;
        if (!bank_journal_id) {
            return;
        }
        var read_res = await this.orm.call(
            "account.journal",
            "read",
            [
                [bank_journal_id],
                // fields defined in account_usability_akretion
                ["bank_default_account_balance", "bank_currency_id"],
            ]
        );
        this.state.journalBalance = read_res[0].bank_default_account_balance;
        this.state.currency = read_res[0].bank_currency_id[0];
    },

});
