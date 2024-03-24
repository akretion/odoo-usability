# Copyright (C) 2016-2024 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'MRP Average Cost',
    'version': '14.0.1.0.0',
    'category': 'Manufactuing',
    'license': 'AGPL-3',
    'summary': 'Update standard_price upon validation of a manufacturing order',
    'description': """
MRP Average Cost
================

I initially developped this module for Odoo 12.0, when the module mrp_account didn't exist, so Odoo didn't support the update of the standard cost of a manufactured product.

In the mrp_account module, you must use workcenters to take the labor costs into account. This module aims at encoding theorical labor costs on the BOM and using it to compute the cost of the finished product.

With this module, when you validate a manufacturing order of a product that has costing method = 'average', the standard_price of the product will be updated by taking into account the standard_price of each raw material and also a number of work hours defined on the BOM plus the extra cost defined of the BOM.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['mrp'],
    'data': [
        'security/mrp_average_cost_security.xml',
        'security/ir.model.access.csv',
        'data/mrp_data.xml',
        'views/mrp_view.xml',
        ],
    'installable': True,
}
