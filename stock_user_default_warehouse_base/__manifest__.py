# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Default Stock Warehouse on User',
    'version': '10.0.1.0.0',
    'category': 'Inventory, Logistics, Warehousing',
    'license': 'AGPL-3',
    'summary': 'Configure a default warehouse on user',
    'description': """
Default Warehouse on User
=========================

With this module, you will be able to configure a default warehouse in the preferences of the user.

This module doesn't do anything by itself. It should be used together with stock_user_default_warehouse_sale and/or stock_user_default_warehouse_purchase.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [
        'users_view.xml',
        ],
    'installable': True,
}
