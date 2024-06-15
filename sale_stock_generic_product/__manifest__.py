# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Stock Generic Product',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Generic products for sale orders',
    'author': 'Akretion',
    'maintainers': ['alexis-via'],
    "development_status": "Mature",
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['sale_stock'],
    'data': ['views/stock_move_line.xml'],
    'installable': True,
}
