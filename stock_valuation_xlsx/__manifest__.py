# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Valuation XLSX',
    'version': '10.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Generate XLSX reports for past or present stock levels',
    'description': """
Stock Valuation XLSX
====================

This module generate nice XLSX stock valuation reports either:

* from a physical inventory,
* from present stock levels (i.e. from quants),
* from past stock levels.

It has several options:

* filter per product category,
* split by lots,
* split by stock location,
* display subtotals per category.

You can access this XLSX stock valuation report either:

* from the menu *Inventory > Reports > Stock Valuation XLSX* (it replaces the native menu *Inventory at Date*)
* from the form view of *validated* inventories (menu *Inventory > Inventory Control > Inventory Adjustments*) via the button *XLSX Valuation Report*.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['stock_account'],
    'data': [
        'wizard/stock_valuation_xlsx_view.xml',
        'views/stock_inventory.xml',
        ],
    'installable': True,
}
