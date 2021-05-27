# Copyright 2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale MRP Usability',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on sale_mrp module',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'sale_mrp',
        'stock_usability',
        ],
    'data': [
        # Native in v14. Do no up-port to v14
        'views/mrp_production.xml',
        'views/sale_order.xml',
        ],
    'installable': True,
}
