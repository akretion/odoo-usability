# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Default Warehouse on User (MRP)',
    'version': '12.0.1.0.0',
    'category': 'Manufacturing',
    'license': 'AGPL-3',
    'summary': "Use the users's default warehouse on manufacturing orders",
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mrp', 'stock_user_default_warehouse_base'],
    'installable': True,
}
