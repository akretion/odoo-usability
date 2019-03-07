# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'POS No Product Template Menu',
    'version': '12.0.1.0.0',
    'category': 'Point of sale',
    'license': 'AGPL-3',
    'summary': "Replace product.template menu entries by product.product menu",
    'description': """
POS No Product Template
=======================

This module replaces the menu entry for product.template by menu entries
for product.product in the *Point Of Sale > Product* menu.

This module also switches to the tree view by default
for Product menu entries, instead of the kanban view.

This module has been written by David Béal
from Akretion <david.beal@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale', 'sale_purchase_no_product_template_menu'],
    'auto_install': True,
    'data': ['pos_view.xml'],
    'installable': True,
}
