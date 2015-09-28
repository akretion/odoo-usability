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
    'summary': "Use only if you don't use variants of products",
    'description': """
Sale Purchase No Product Template
=================================

You may use this module only if you don't use product variants i.e. you don't have (and don't plan to have in the future) several product.product attached to one product.template.

This module replaces the menu entries for product.template by menu entries for product.product in the *Sales*, *Purchases* and *Warehouse* menu entry.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase', 'sale'],
    'data': ['view.xml'],
    'installable': True,
}
