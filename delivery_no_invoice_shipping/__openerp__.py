# -*- encoding: utf-8 -*-
##############################################################################
#
#    Delivery No Invoice Shipping module for Odoo
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
    'name': 'Delivery No Invoice Shipping',
    'version': '0.1',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'When invoicing from delivery, do not add shipping costs',
    'description': """
Delivery No Invoice Shipping
============================

By default, when the delivery module is installed and you create an invoice from a delivery picking, Odoo will add an invoice line for the shipping costs if there is not already such a line in the order. This module avoids that: no additionnal invoice line will be added when invoicing from delivery.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['delivery'],
    'data': [],
    'installable': True,
}
