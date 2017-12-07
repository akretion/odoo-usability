# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Point of Sale Usability',
    'version': '10.0.0.2.0',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in Point of Sale',
    'description': """
Point of Sale Usability
=======================

Minor usability enhancements in POS:

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'point_of_sale',
        'product_usability',  # I need it for the groupby on the search view product.product_template_search_view
        ],
    'data': [
        'pos_view.xml',
        'product_view.xml',
        ],
    'installable': True,
}
