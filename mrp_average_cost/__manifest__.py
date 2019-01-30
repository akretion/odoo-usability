# -*- coding: utf-8 -*-
# Copyright (C) 2016-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP Average Cost',
    'version': '12.0.1.0.0',
    'category': 'Manufactuing',
    'license': 'AGPL-3',
    'summary': 'Update standard_price upon validation of a manufacturing order',
    'description': """
MRP Average Cost
================

By default, the official stock module updates the standard_price of a product that has costing_method = 'average' when validating an incoming picking. But the official 'mrp' module doesn't do that when you validate a manufactuging order.

This module adds this feature : when you validate a manufacturing order of a product that has costing method = 'average', the standard_price of the product will be updated by taking into account the standard_price of each raw material and also a number of work hours defined on the BOM.

Together with this module, I recommend the use of my module product_usability, available in the same branch, which contains a backport of the model product.price.history from v8 to v7.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mrp'],
    'data': [
        'mrp_view.xml',
        'mrp_data.xml',
        'security/labour_cost_profile_security.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
