# -*- coding: utf-8 -*-
# Copyright (C) 2015 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Procurement Usability',
    'version': '10.0.1.0.0',
    'category': 'Hidden/Dependency',
    'license': 'AGPL-3',
    'summary': 'Display fields in form view of procurement order',
    'description': """
Procurement Usability
======================

This module display several fields in the form view of procurement order (link to sale order line, stock moves), that are very useful for deep analysis of procurement orders and debugging.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['procurement'],
    'data': [
        'procurement_view.xml',
        'wizard/procurement_mass_cancel_view.xml',
        ],
    'installable': True,
}
