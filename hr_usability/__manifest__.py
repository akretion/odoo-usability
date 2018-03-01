# -*- coding: utf-8 -*-
# Copyright 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'HR Usability',
    'version': '10.0.1.0.0',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'summary': 'Better usability in HR module',
    'description': """
HR Usability
============

The HR module from the official addons adds a field *bank_account_id*. But, if you want to pay an expense note via SEPA Credit Transfer, Odoo doesn't use the bank account of the Employee, but the bank account configured on the Partner. So this module hides this field.

This module has been developped by Alexis de Lattre <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['hr'],
    'data': [
        'hr_view.xml',
        ],
    'installable': True,
}
