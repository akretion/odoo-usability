# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product Manager Group module for OpenERP
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
    'name': 'Product Manager Group',
    'version': '0.1',
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
    'active': False,
    'installable': False,
}
