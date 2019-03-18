# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Financial Report Qweb Usability',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account_financial_report_qweb module',
    'description': """
Account Financial Report Usability
==================================

The usability enhancements include:
TODO

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'account_financial_report_qweb',
        ],
    'data': [
        'views/reports.xml',
        'views/layouts.xml',],
    'installable': True,
}
