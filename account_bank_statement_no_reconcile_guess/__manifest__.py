# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Bank Statement No Reconcile Guess',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': "Don't pre-select lines to reconcile in bank statements",
    'description': """
Account Bank Statement No Reconcile Guess
=========================================

Here is a scenario where the "reconcile guess" feature is a problem for the accountant:

1) The accountant imports a large bank statement with 40 bank statement lines.
2) The "reconcile guess" feature will pre-select reconcile of line X with line 39 of the bank statement. But this guess is a mistake and line X should be reconciled with line 2 of the bank statement.
=> The accountant will not understand why he can't select line X to be reconciled with line 2 of the bank statement. To be able to reconcile line 2 correctif, he has to:
3) click several times on the "next page" button to reach line 39 of the bank statement and unselect line X.
4) Go back to line 2 of the bank statement and now he will be able to select line X.

This module disables the "reconcile guess" feature to avoid this problem.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'data': [],
    'installable': True,
}
