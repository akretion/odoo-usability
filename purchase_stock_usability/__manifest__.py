# Copyright (C) 2014-2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Stock Usability',
    'version': '14.0.1.0.0',
    'category': 'Purchases',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on purchase_stock module',
    'description': """
Purchase Stock Usability
========================

Several usability improvements on the official purchase_stock module:

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'purchase_stock',
        'purchase_usability',
        ],
    'data': [
        'views/stock_picking.xml',
        ],
    'installable': True,
}
