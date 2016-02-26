# -*- coding: utf-8 -*-
##############################################################################
#
#    MRP Average Cost module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'MRP Average Cost',
    'version': '0.1',
    'category': 'Manufactuing',
    'license': 'AGPL-3',
    'summary': 'Update standard_price upon validation of a manufacturing order',
    'description': """
MRP Average Cost
================

By default, the official stock module updates the standard_price of a product that has costing_method = 'average' when validating an incoming picking. But the official 'mrp' module doesn't do that when you validate a manufactuging order.

This module adds this feature : when you validate a manufacturing order of a product that has costing method = 'average', the standard_price of the product will be updated by taking into account the standard_price of each raw material and also a number of work hours defined on the BOM.

Together with this module, I recommend the use of my module product_usability, available in the same branch, which contains a backport of the model product.price.history from v8 to v7.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
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
