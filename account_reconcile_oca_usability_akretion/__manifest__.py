# Copyright 2026 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Reconcile OCA Usability Akretion',
    'version': '18.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in OCA bank reconcile interface',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['account_reconcile_oca'],
    'data': [],
    "assets": {
        "web.assets_backend": [
            "account_reconcile_oca_usability_akretion/static/src/js/reconcile_controller_patch.esm.js",
        ],
    },
    'installable': True,
}
