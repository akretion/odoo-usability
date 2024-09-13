# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Payment Line Manual Account',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Ability to select the account on payment lines without journal item',
    'description': """
With this module, when you manually create a payment line that is not linked to a journal item, you can select an account (by default, it is set to the payable/receivable account of the partner) : this account will be used as the counter part of the outbound/inbound payment account configured on the bank journal. It covers special needs of a few companies that use SEPA credit transfer for the same partner in different accounting scenarios.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'maintainers': ['alexis-via'],
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['account_payment_order'],
    'data': [
        "views/account_payment_line.xml",
    ],
    'installable': True,
}
