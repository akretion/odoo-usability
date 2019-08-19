# Copyright 2015-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Usability',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account module',
    'description': """
Account Usability
=================

The usability enhancements include:
* show the supplier invoice number in the tree view of supplier invoices
* add an *Overdue* filter on invoice search view (this feature was previously 
  located in te module *account_invoice_overdue_filter*)
* increase the default limit of 80 lines in account move and account move line view.
* fast search on *Reconcile Ref* for account move line.
* disable reconciliation "guessing"
* add sale dates to invoice report to be compliant with
  https://www.service-public.fr/professionnels-entreprises/vosdroits/F31808

Together with this module, I recommend the use of the following modules:
* account_invoice_supplier_ref_unique (OCA project account-invoicing)
* account_move_line_no_default_search (OCA project account-financial-tools)
* invoice_fiscal_position_update (OCA project account-invoicing)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'account',
        'base_view_inheritance_extension',
        'base_usability',  # needed only to access base_usability.group_nobody
                           # in v12, I may create a module only for group_nobody
        ],
    'data': [
        'account_view.xml',
        'account_report.xml',
        'account_invoice_report_view.xml',
        'partner_view.xml',
        'wizard/account_invoice_mark_sent_view.xml',
        'report/invoice_report.xml',
        ],
    'installable': True,
}
