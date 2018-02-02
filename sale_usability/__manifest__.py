# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Usability',
    'version': '10.0.0.1.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Show invoices on sale orders',
    'description': """
Sale Usability Extension
========================

Several small usability improvements:

* Display amount untaxed in tree view
* TODO: update this list

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
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
