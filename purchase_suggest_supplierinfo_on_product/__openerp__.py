# -*- coding: utf-8 -*-
# © 2016 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Purchase Suggest Supplierinfo on Product',
    'summary': 'Replace orderpoints by supplierinfo on product',
    'version': '8.0.1.0.0',
    'category': 'Purchase Management',
    'website': 'http://akretion.com',
    'author': 'Akretion',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'purchase_suggest',
        'product_variant_supplierinfo'
    ],
    'data': [
        'wizard/purchase_suggest_view.xml',
    ]
}
