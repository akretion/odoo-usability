# Copyright 2014-2024 Akretion (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Purchase Usability',
    'version': '18.0.1.0.0',
    'category': 'Purchases',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on purchase module',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order.xml',
        'views/purchase_report.xml',
        'views/account_move.xml',
        ],
    'installable': True,
}
