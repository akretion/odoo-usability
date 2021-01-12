# -*- coding: utf-8 -*-
# Copyright 2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Account Usability',
    'version': '10.0.1.0.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements in stock_account',
    'description': """
Stock Account Usability
========================

The usability enhancements inclure:
* show property_cost_method on product form

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock_account'],
    'data': ['product_view.xml'],
    'installable': True,
}
