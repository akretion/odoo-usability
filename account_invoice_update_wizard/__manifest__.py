# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2018-2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Update Wizard',
    'version': '14.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Wizard to update non-legal fields of an open/paid invoice',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_move_update_view.xml',
        'views/account_move.xml',
    ],
    'installable': True,
}
