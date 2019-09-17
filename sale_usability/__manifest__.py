# Copyright 2014-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Usability',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on sale module',
    'description': """
Sale Usability
==============

This module provides several small usability improvements on the official *sale* module:

* Display amount untaxed in tree view
* TODO: update this list

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'sale',
        'base_view_inheritance_extension',
        ],
    'data': [
        'sale_view.xml',
        'sale_report_view.xml',
        'product_view.xml',
        'account_invoice_view.xml',
        ],
    'installable': True,
}
