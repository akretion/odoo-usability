# Copyright 2016-2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP No Product Template Menu',
    'version': '12.0.1.0.0',
    'category': 'Manufacturing',
    'license': 'AGPL-3',
    'summary': "Replace product.template menu entries by product.product menu",
    'description': """
MRP No Product Template
=======================

This module replaces the menu entry for product.template by menu entries
for product.product in the *Manufacturing > Master Data* menu.

This module also switches to the tree view by default
for Product menu entries, instead of the kanban view.

This module has been written by Alexis de Lattre
from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mrp', 'sale_purchase_no_product_template_menu'],
    'auto_install': True,
    'data': ['mrp_view.xml'],
    'installable': True,
}
