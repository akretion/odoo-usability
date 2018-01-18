# -*- coding: utf-8 -*-
# © 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>


{
    'name': 'Stock My Operations Filter',
    'version': '10.0.0.1.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': "Adds a filter 'My Operations'",
    'description': """
When you have several warehouses, you have a lot of Stock Operations Types, and the menu *Warehouse > All Operations* becomes difficult to use because there are too many types of operations. This module solves this problem: it adds a filter 'My Operations' on stock.picking.type, which is active by default when you go to Warehouse > All Operations. This filter is configurable for each user.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [
        'stock_view.xml',
        'users_view.xml',
    ],
    'installable': True,
}
