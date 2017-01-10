# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Usability',
    'version': '0.1',
    'category': 'Sale Management',
    'license': 'AGPL-3',
    'summary': 'Show invoices on sale orders',
    'description': """
Sale Usability Extension
========================

Several small usability improvements:

* Display Invoices on Sale Order form view (in dedicated tab).
* Display currency in tree view

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': [
        'sale_view.xml',
        'product_view.xml',
        ],
    'installable': True,
}
