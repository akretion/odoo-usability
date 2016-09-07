# -*- coding: utf-8 -*-
# © 2013-TODAY Akretion (http://www.akretion.com)
#   @author Florian da Costa <florian.dacosta@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Product Search Supplier Code',
    'version': '0.1',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': "Allow to search product by its suppliers'code",
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product', 'stock'],
    'data': [
        'views/product_view.xml',
        'views/picking_view.xml',
    ],
    'installable': True,
    'active': False,
}
