# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Default Stock Warehouse on User',
    'version': '12.0.1.0.0',
    'category': 'Inventory, Logistics, Warehousing',
    'license': 'AGPL-3',
    'summary': 'Configure a default warehouse on user',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': [
        'views/users_view.xml',
    ],
    'installable': True,
}
