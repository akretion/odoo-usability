# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Stock No Product Template Menu',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'license': 'AGPL-3',
    'summary': "Replace product.template menu entries by product.product menu entries",
    'description': """
Stock No Product Template
=========================

This module replaces the menu entries for product.template by menu entries for product.product in the *Inventory* menu entry. With this module, the only menu entry for product.template is in the menu *Sales > Configuration > Product Categories and Attributes*.

This module also switches to the tree view by default for Product menu entries, instead of the kanban view.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': ['view.xml'],
    'installable': True,
}
