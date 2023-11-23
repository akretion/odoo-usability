# Copyright 2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product Priority Star',
    'version': '14.0.1.0.0',
    'category': 'Product',
    'license': 'AGPL-3',
    'summary': 'Add a priority star on product',
    'description': """
Product Priority Star
=====================

This module adds a priority star on products (like on pickings and manufacturing order). If the star is yellow, the product will be displayed at the top.

This feature is native in Odoo 16.0.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['product'],
    'excludes': ['product_priority'],
    'data': ['views/product_template.xml'],
    'installable': True,
}
