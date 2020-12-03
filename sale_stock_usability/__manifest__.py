# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Sale Stock Usability',
    'version': '14.0.1.0.0',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'Small usability improvements to the sale_stock module',
    'description': """
Sale Stock Usability
====================

The usability enhancements include:

* TODO update the list

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_stock'],
    'data': [
        'views/sale_order.xml',
        'views/procurement_group.xml',
        'views/stock_move.xml',
        'views/stock_picking.xml',
        ],
    'installable': True,
}
