# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Purchase No Product Template Menu',
    'version': '12.0.1.0.0',
    'category': 'Sale and Purchase',
    'license': 'AGPL-3',
    'summary': "Replace product.template menu entries by product.product menu entries",
    'description': """
Sale Purchase No Product Template
=================================

This module replaces the menu entries for product.template by menu entries for product.product in the *Sales*, *Purchases* and *Warehouse* menu entry. With this module, the only menu entry for product.template is in the menu *Sales > Configuration > Product Categories and Attributes*.

This module also switches to the tree view by default for Product menu entries, instead of the kanban view.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'purchase',
        'sale',
        ],
    'data': ['view.xml'],
    'installable': True,
}
