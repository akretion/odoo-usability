# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock History ODS',
    'version': '10.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Adds a Py3o ODS report on Inventory at Date',
    'description': """
Stock History ODS
=================

This module will add a Py3o ODS report on Inventory at Date.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['stock_account', 'report_py3o'],
    'data': [
        'report.xml',
        'wizard/wizard_valuation_history_view.xml',
        ],
    'installable': True,
}
