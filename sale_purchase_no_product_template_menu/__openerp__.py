# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Purchase No Product Template Menu module for Odoo
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
    'name': 'Sale Purchase No Product Template Menu',
    'version': '0.1',
    'category': 'Sale and Purchase',
    'license': 'AGPL-3',
    'summary': "Remplace product.template menu entries by product.product menu entries",
    'description': """
Sale Purchase No Product Template
=================================

This module replaces the menu entries for product.template by menu entries for product.product in the *Sales*, *Purchases* and *Warehouse* menu entry. With this module, the only menu entry for product.template is in the menu *Sales > Configuration > Product Categories and Attributes*.

This module also switches to the tree view by default for Product menu entries, instead of the kanban view.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase', 'sale', 'base_usability'],
    'data': ['view.xml'],
    'installable': True,
}
