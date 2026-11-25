# Copyright 2014-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Quant Apply Inventory User',
    'version': '16.0.1.0.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Allow correction of stock levels by stock users',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['stock'],
    'data': [
        'views/stock_quant.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
