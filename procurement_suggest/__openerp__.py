# -*- encoding: utf-8 -*-
##############################################################################
#
#    Procurement Suggest module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
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
    'name': 'Procurement Suggest',
    'version': '0.1',
    'category': 'Procurements',
    'license': 'AGPL-3',
    'summary': 'Suggest POs/MOs from special suggest orderpoints',
    'description': """
Procurement Suggest
===================

TODO

Roadmap : split the module in 2 and move the purchase-specific part in a module
that has a dependancy on this module and purchase. This module will then not have a depandancy on purchase any more.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock', 'purchase'],
    'data': [
        'stock_view.xml',
        'wizard/procurement_suggest_view.xml',
        ],
    'installable': True,
}
