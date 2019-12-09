# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Commission Simple Sale',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Give access to commission results to Salesman',
    'description': """
Commission Simple Sale
======================

This module allows salesman to see their commissions in Odoo, under the Sales menu.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'sale',
        'commission_simple',
        ],
    'data': [
        'views/commission.xml',
        'security/rule.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
