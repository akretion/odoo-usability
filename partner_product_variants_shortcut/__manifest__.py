# -*- coding: utf-8 -*-
##############################################################################
#
#    Partner Product Variants Shortcut module for Odoo
#    Copyright (C) 2014-2016 Akretion (http://www.akretion.com)
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
    'name': 'Partner Product Variants Shortcut',
    'version': '0.1',
    'category': 'Contact Management',
    'license': 'AGPL-3',
    'summary': 'Adds a shortcut on partner form to the products supplied by this partner',
    'description': """
Partner Product Variants Shortcut
=================================

Adds a shortcut on supplier partner form to the products supplied by this partner (display the product variants view).

This module is an alternative to the module *partner_products_shortcut* ; the only difference is that it displays the product variants view (product.product) instead of the product view (product.template).

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
    'conflicts': ['partner_products_shortcut'],
    'data': ['partner_view.xml'],
    'installable': False,
}
