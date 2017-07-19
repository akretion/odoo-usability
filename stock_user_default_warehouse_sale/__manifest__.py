# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Default Warehouse on User (Sale)',
    'version': '10.0.1.0.0',
    'category': 'Sale Management',
    'license': 'AGPL-3',
    'summary': "Use the users's default warehouse on sale orders",
    'description': """
Default Warehouse on User (Sale)
================================

The default warehouse configured in the preferences of the user will be used by default on sale orders.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_stock', 'stock_user_default_warehouse_base'],
    'installable': True,
}
