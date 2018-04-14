# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Generate Price Weight Barcode',
    'version': '10.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': 'Add a wizard to print product barcode stickers on ZPL printer',
    'description': """
Print product barcode stickers on ZPL printer
=============================================

This module adds a wizard on product.product form view which allows to generate and print a product barcode sticker on a ZPL printer (such as Zebra GC420, GK420, ...). It can print:

* regular product barcode stickers. These stickers will show:
  * product name
  * product price
  * EAN13 barcode

* price/weight barcode stickers. These stickers will show:
  * product name
  * weight (the wizard asks for this info)
  * price
  * price per kg
  * EAN13 barcode

Roadmap: It would be cool one to day use the OCA module *printer_zpl2* or the underlying *zpl2* lib.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    # We depend on point_of_sale and not only 'product'
    # because the weight barcode rules are added by the point_of_sale module
    'depends': [
        'point_of_sale',
        'barcodes',
        'base_report_to_printer',
        ],
    'data': [
        'wizard/product_print_zpl_barcode_view.xml',
        'views/product.xml',
    ],
    'installable': True,
}
