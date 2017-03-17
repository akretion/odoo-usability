# -*- coding: utf-8 -*-
# © 2017 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Unit Manager Group',
    'summary': 'Add a group Product Unit of Measure Manager',
    'version': '8.0.1.0.0',
    'category': 'Product',
    'website': 'http://akretion.com',
    'author': 'Akretion',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'sale',
        'purchase',
        'mrp',
    ],
    'data': [
        'security/product_security.xml',
        'security/ir.model.access.csv',
        'views/product_view.xml',
    ],
}
