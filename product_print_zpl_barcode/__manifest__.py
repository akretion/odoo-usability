# Copyright 2016-2020 Akretion (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Generate Price Weight Barcode',
    'version': '14.0.1.0.0',
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

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    # We depend on point_of_sale and not only 'product'
    # because the price barcode rule is added by the point_of_sale module
    # (the weight barcode rule is added by the stock module)
    'depends': [
        'point_of_sale',
        'barcodes',
        'base_report_to_printer',
        ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_print_zpl_barcode_view.xml',
        'views/product.xml',
    ],
    'installable': True,
}
