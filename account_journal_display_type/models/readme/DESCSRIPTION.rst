This module introduce improvement on journal type to simplify configuration of Payment and Cash Journal.


The payment journal does not exist in odoo, it's associate to a bank journal but in payment case, 
the default_account_id will have the same value as payment_debit_account_id.
This module introduce a new field type called display_type who hide the default type from UI, and make possible to had new journal type. Payment display_type is hadded here, and the associated legacy journal type is bank. The default_account_id is hided and will have the same value as payment_debit_account_id

For Cash type, the only field we kept is default_account_id. The payment config tab is useless for a cash journal and was remove from UI. (in this case payment_debit_account_id and payment_credit_account_id are set with value of default_account_id)
