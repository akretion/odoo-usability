# -*- coding: utf-8 -*-
##############################################################################
#
#    POS No Product Template Menu module for Odoo
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
    'name': 'POS No Product Template Menu',
    'version': '0.1',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': "Remplace product.template menu entry by product.product in POS",
    'description': """
POS No Product Template
=======================

This module replaces the menu entry for product.template by a menu entry for product.product in the *Point of Sale*.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale', 'pos_usability'],
    # pos_usability is required to have the filter available_in_pos
    'data': ['view.xml'],
    'installable': False,
}
