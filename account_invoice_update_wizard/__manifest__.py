# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Account Invoice Update Wizard',
    'version': '11.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Wizard to update non-legal fields of an open/paid invoice',
    'author': 'Akretion',
    'website': 'http://github.com/akretion/odoo-usability',
    'depends': [
        'account',
    ],
    'data': [
        'wizard/account_invoice_update_view.xml',
        'views/account_invoice.xml',
    ],
}
