This module introduces improvements to the journal type, simplifying the configuration of payment and cash journals.


The payment journal does not exist in Odoo; it is associated with a bank journal, but in the case of payments, 
Tthe default_account_id will have the same value as payment_debit_account_id.
This module introduces a new field type called 'display_type' which hides the default type from the UI and makes it possible to add new journal types. The payment display type has been added here, and the associated legacy journal type is bank. The 'default_account_id' field is hidden and will have the same value as 'payment_debit_account_id'.

For the cash type, the only field that has been kept is the default_account_id. The Payment Configuration tab is no longer useful for a cash journal, so it has been removed from the user interface. In this case, payment_debit_account_id and payment_credit_account_id are set to the value of default_account_id.