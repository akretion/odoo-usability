# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale from Private Stock',
    'version': '10.0.1.0.0',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'Sell from private stock',
    'description': '''
Sale from Private Stock
=======================

This module is particularly useful for companies that lend stock to their distributors and when it's too heavy to create a new warehouse for each distributor.

This module allows to define a private stock location on a customer.

On a sale order, there is a new optional field to define the source stock location. On a sale order, if you select a customer that has a private stock location, this private stock location will be set as the source stock location of the sale order (but you can change it).


This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    ''',
    'author': 'Akretion',
    'depends': ['sale_stock'],
    'data': [
        'stock_view.xml',
        'stock_data.xml',
        'partner_view.xml',
        ],
    'installable': True,
}
