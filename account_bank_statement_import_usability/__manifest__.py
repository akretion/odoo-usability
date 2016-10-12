# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Bank Statement Import Usability',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account_bank_statement_import module',
    'description': """
Account Bank Statement Import Usability
=======================================

This module adds the following changes:

* Works if the bank statement file only contain the account number and not the full IBAN

* remove start balance and end balance (doesn't work with OFX, which is one of the most used file format !)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_bank_statement_import'],
    'data': ['account_view.xml'],
    'installable': True,
}
