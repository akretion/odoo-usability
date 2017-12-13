# -*- coding: utf-8 -*-
# © 2016-2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Fiscal Position Payable Receivable',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Configure payable/receivable accounts on fiscal positions',
    'description': """
Account Fiscal Position Payable Receivable
==========================================

This module allows to configure a special *Partner Receivable Account* and a special *Partner Payable Account* on fiscal positions. This is used in the onchange of the fiscal position of partners.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'data': [
        'account_fiscal_position_view.xml',
    ],
    'installable': True,
}
