# coding: utf-8
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Purchase Usability Extension',
    'version': '0.1',
    'category': 'Purchase Management',
    'license': 'AGPL-3',
    'summary': 'Show invoices and receptions on PO',
    'description': """
Purchase Usability Extension
============================

- Display Invoices and Incoming Shipments on Purchase Order form view
  (in dedicated tabs).
- Add a dedicated menu and tree view to Product Supplier Info model.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com>
for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase'],
    'data': [
        'purchase_view.xml',
        'stock_view.xml',
        'supplierinfo_view.xml',
    ],
    'active': False,
}
