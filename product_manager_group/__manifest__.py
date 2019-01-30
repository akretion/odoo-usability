# -*- coding: utf-8 -*-
# Copyright 2014-2019 Akretion
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Manager Group',
    'version': '12.0.1.0.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Add a group Product Manager',
    'description': """
Product Manager Group
=====================

This module adds a group Product Manager. This group used to exist in older versions of OpenERP (5.0, 6.0) but was unfortunately removed in OpenERP 6.1. This module restores this group.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
    'data': [
        'security/product_security.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
