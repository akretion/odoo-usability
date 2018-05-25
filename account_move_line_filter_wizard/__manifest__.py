# -*- coding: utf-8 -*-
# Copyright (C) 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Move Line Filter Wizard',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Easy and fast access to the details of an account',
    'description': """
Account Move Line Filter Wizard
===============================

This module adds a wizard in Accounting > ... > 

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_usability'],
    'data': ['wizard/account_move_line_filter_view.xml'],
    'installable': True,
}
