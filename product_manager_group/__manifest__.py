# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Manager Group',
    'version': '10.0.0.1.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Add a group Product Manager',
    'description': """
Product Manager Group
=====================

This module adds a group Product Manager. This group used to exist in older versions of OpenERP (5.0, 6.0) but was unfortunately removed in OpenERP 6.1. This group restores this group.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
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
