# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Expiry Simple',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'license': 'AGPL-3',
    'summary': 'Simpler and better alternative to the official product_expiry module',
    'description': """
Product Expiry Simple
=====================

This module is similar to the official *product_expiry* modules, but much simpler and much better:

* Only one expiry date field instead of 4 !
* date field instead of datetime
* No automatic computing of expiry date based on a delay configured on product (not needed in most companies)
* colored production lot and stock quant tree views depending on expiry dates
* ability to show stats about expiry dates on quants pivot table (thanks to related stored field on stock.quant)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'conflicts': ['product_expiry'],
    'data': [
        'stock_view.xml',
        'product_removal_data.xml',
        ],
    'installable': True,
}
