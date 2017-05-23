# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Import French HSBC Card Bank Statements',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'summary': 'Import French HSBC Card Bank Statements in Odoo (CSV version)',
    'depends': ['account_bank_statement_import'],
    'data': ['views/account_bank_statement_import.xml'],
    'installable': True,
}
