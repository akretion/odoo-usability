# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Tracking UL module for OpenERP
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
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
    'name': 'Stock Tracking UL',
    'version': '0.1',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Link stock.tracking to product.ul',
    'description': """
This module adds a link from stock.tracking to product.ul. It also adds
the properties of stock.ul that are present in OpenERP 8 and not present
in OpenERP 7 (weight, width, length, height). This will be required for
UPS webservices, which need to know the size of each package.

So this module should NOT be used on v8, only on v7.

This module has been written by Alexis de Lattre
from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['delivery'],
    'data': ['stock_view.xml', 'product_view.xml'],
    'installable': True,
}
