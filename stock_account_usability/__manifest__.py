# Copyright 2019-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Account Usability',
    'version': '14.0.1.0.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements on stock_account',
    'description': """
Stock Account Usability
=======================

The usability enhancements include:

- show to_refund on stock.move form view

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock_account', 'stock_usability'],
    'data': [
        'views/stock_move.xml',
        'views/product.xml',
        ],
    'installable': False,
}
