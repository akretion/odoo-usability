# -*- encoding: utf-8 -*-
##############################################################################
#
#    Procurement Usability module for Odoo
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
    'name': 'Procurement Usability',
    'version': '0.1',
    'category': 'Hidden/Dependency',
    'license': 'AGPL-3',
    'summary': 'Display fields in form view of procurement order',
    'description': """
Procurement Usability
======================

This module display several fields in the form view of procurement order (link to sale order line, stock moves), that are very useful for deep analysis of procurement orders and debugging.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_stock'],
    'data': ['procurement_view.xml'],
    'installable': True,
}
