# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Analytic Analysis Usability',
    'version': '8.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on Account Analytic Analysis',
    'description': """
Account Analytic Analysis Usability
===================================

Usability improvements include:

* add next invoice date in tree view of contrats (and add a group by)

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_analytic_analysis'],
    'data': [
        'analytic_view.xml',
    ],
    'installable': True,
}
