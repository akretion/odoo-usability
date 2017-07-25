# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Usability module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Account Usability',
    'version': '0.3',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account module',
    'description': """
Account Usability
=================

The usability enhancements include:
* show the supplier invoice number in the tree view of supplier invoices
* add an *Overdue* filter on invoice search view (this feature was previously located in te module *account_invoice_overdue_filter*)
* Increase the default limit of 80 lines in account move and account move line view.
* Fast search on *Reconcile Ref* for account move line.
* disable reconciliation "guessing"

Together with this module, I recommend the use of the following modules:
* account_invoice_supplier_ref_unique (OCA project account-invoicing)
* account_move_line_no_default_search (OCA project account-financial-tools)
* invoice_fiscal_position_update (OCA project account-invoicing)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'conflicts': ['account_invoice_overdue_filter'],
    'data': [
        'account_view.xml',
        'wizard/account_invoice_mark_sent_view.xml',
        ],
    'installable': True,
}
