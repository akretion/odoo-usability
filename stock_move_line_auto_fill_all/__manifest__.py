# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Move Line Auto-fill All',
    'version': '14.0.1.0.0',
    'category': 'Warehouse',
    'license': 'AGPL-3',
    'summary': 'Add button on picking to auto-fill done qty',
    'description': """
This module is an alternative to the OCA module **stock_move_line_auto_fill** from https://github.com/OCA/stock-logistics-workflow/
The OCA module doesn't auto-fill the stock move lines with lots. This module does.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'maintainers': ['alexis-via'],
    "development_status": "Mature",
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['stock'],
    'data': [
        'views/stock_picking.xml',
    ],
    'installable': True,
}
