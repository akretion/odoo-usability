# Copyright (C) 2014-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Usability',
    'version': '14.0.1.0.0',
    'category': 'Purchases',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on purchase module',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order.xml',
        'views/purchase_report.xml',
        ],
    'installable': True,
}
