# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Cutoff Accrual Picking ODS',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Adds an Aeroo ODS report on cutoff accrual',
    'description': """
Account Cutoff Accrual Picking ODS
==================================

This module will add an Aeroo ODS report on Accrued Revenue and Accrued Expense.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['account_cutoff_accrual_picking', 'report_aeroo'],
    'data': ['report.xml'],
    'installable': True,
}
