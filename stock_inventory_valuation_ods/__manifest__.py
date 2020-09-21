# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Inventory Valuation ODS',
    'version': '10.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Adds a Py3o ODS report on inventories',
    'description': """
Stock Inventory Valuation ODS
=============================

This module will add a Py3o ODS report on Stock Inventories.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['stock_inventory_valuation', 'report_py3o'],
    'data': ['report.xml'],
    'installable': True,
}
