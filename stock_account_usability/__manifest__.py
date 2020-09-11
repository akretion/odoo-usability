# -*- coding: utf-8 -*-
# Copyright 2019-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Account Usability',
    'version': '12.0.1.0.0',
    'category': 'Hidden',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements on stock_account',
    'description': """
Stock Account Usability
=======================

The usability enhancements include:

* activate the refund option by default in return wizard on pickings

* show field *property_cost_method* on product form view

* add ability to select a stock location on the inventory valuation report


This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock_account'],
    'data': [
        'product_view.xml',
        'wizard/stock_quantity_history_view.xml',
        ],
    'installable': True,
}
