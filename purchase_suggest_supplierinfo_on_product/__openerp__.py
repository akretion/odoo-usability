# -*- coding: utf-8 -*-

{
    'name': 'Purchase Suggest Supplierinfo on Product',
    'version': '0.1',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'summary': 'Replace orderpoints by supplierinfo on product',
    'description': """
Purchase Suggest Supplierinfo on Product
========================================

With this module, instead of using orderpoints, we use supplierinfos on product.

This module has been written by Chafique DELLI from Akretion <chafique.delli@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase_suggest', 'product_variant_supplierinfo'],
    'data': [
        'wizard/purchase_suggest_view.xml',
        ],
    'installable': True,
}
