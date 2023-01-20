# Copyright 2023 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Detailed Type',
    'version': '14.0.1.0.0',
    'category': 'Product',
    'license': 'LGPL-3',
    'summary': 'Backport detailed_type from v16 to v14',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['product'],
    'data': [
        'views/product.xml',
        ],
    'post_init_hook': 'set_product_detailed_type',
    'installable': True,
}
