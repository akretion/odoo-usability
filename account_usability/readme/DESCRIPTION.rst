This modules adds the following functions:

* Add an *Overdue* filter on invoice search view (this feature was previously 
  located in te module *account_invoice_overdue_filter*)
* Increase the default limit of 80 lines in account move and account move line view.
* disable reconciliation "guessing"
* fast search on *Reconcile Ref* for account move line.
* add sale dates to invoice report to be compliant with
  https://www.service-public.fr/professionnels-entreprises/vosdroits/F31808
* Sale date on qweb invoices
* A wizard to mark several invoices as sent at once (forward from v8)
* Default date for Account Move Reversal is now D+1 instead of today
* Track more fields on invoice (see details in account.py)
* Add boolean fields `has_discount` and `has_attachment` on invoice
* Add button "Delete line qty = 0" on supplier invoice
* Cut name_get() of invoice if too long
* A script for if Odoo screws up invoice attachment filename
* help functions for py3o reports
* Show code on name_get of journal
* add direct search of journal using code
* add copy=False on some fields
* Add unicity constraint on analytic codes per company
* Better default values on account move
* Add link from account move line to invoice
* Add start_date and end_date on bank statements
* Add transfer_account_id to invoicing config page
* Improve domain reconciliation widget
* account.reconcile.model don't copy name to label via onchange
* Add method to get fiscal position without partner_id
* Restore drill-through on sale and invoice reports
* don't attach PDF upon invoice report generation on supplier invoices/refunds
* Add filter on debit and credit amount for Move Lines
* Add supplier invoice number in invoice tree view

Together with this module, I recommend the use of the following modules:

* account_invoice_supplier_ref_unique (OCA project account-invoicing)
* account_move_line_no_default_search (OCA project account-financial-tools)
* invoice_fiscal_position_update (OCA project account-invoicing)
