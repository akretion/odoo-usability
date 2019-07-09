# Copyright 2018-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Delivery Usability',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements in Delivery',
    'description': """
Delivery Usability
===================

The usability enhancements include:
* allow modification of carrier and it's tracking ref. on a done picking
* display field 'invoice_shipping_on_delivery' on sale.order form view

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['delivery'],
    'data': [
        'sale_view.xml',
        'stock_view.xml',
        ],
    'installable': True,
}
