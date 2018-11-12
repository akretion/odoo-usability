# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account No Analytic Tags',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'No Analytic Tags in Accounting',
    'description': """
Account No Analytic Tags
========================

This module hides analytic tags on invoices and move lines.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account', 'base_usability'],
    'data': ['account_view.xml'],
    'installable': True,
}
