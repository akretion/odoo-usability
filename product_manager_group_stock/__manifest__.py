# -*- coding: utf-8 -*-
# © 2014-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Product Manager Group Stock',
    'version': '10.0.1.0.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Extend the group Product Manager to Stock',
    'description': """
Product Manager Group Stock
===========================

Extends the group Product Manager to Stock Management.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product_manager_group', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'auto_install': True,
}
