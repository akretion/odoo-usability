# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Hide Analytic Lines',
    'version': '8.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Hide analytic lines',
    'description': """
Account Hide Analytic Lines
===========================

This module hides analytic lines. If you don't use timesheets, you should
not use analytic lines at all. Instead, you should only use
account move lines with the analytic account field (technical name: *analytic_account_id*).

Why ? Because, when you change the analytic account on an account move line,
the analytic line is not updated by Odoo. So, if you use the report available in *Reporting > Accounting > Analytic Entries Analysis*, as this report is based on analytic lines, the results will not take into account the changes of analytic account that you made on some account move lines.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account', 'base_usability'],
    'data': ['account_view.xml'],
    'installable': False,
}
