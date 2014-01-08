# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Fiscal Position Update Button module for OpenERP
#    Copyright (C) 2011-2014 Julius Network Solutions SARL <contact@julius.fr>
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
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
    'name': 'Sale Fiscal Position Update Button',
    'version': '1.0',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'Update the fiscal position of a sale order in one click',
    'description': """
Sale Fiscal Position Update Button
==================================

When the sale order is in draft/sent state, you can change the fiscal position and click on a button *Update Tax* to update the taxes on all the sale order lines which have a product (if a sale order line doesn't have a product, it won't work and the user will have an error message).

This module is an alternative to the module sale_fiscal_position_update from the sale-wkfl OCA branch, which works with an on_change. It is particularly usefull when a country updates it's VAT rates and the salesman want to update their quote and have the new VAT rates in one click.
""",
    'author': 'Julius Network Solutions, Akretion',
    'depends': ['sale'],
    'data': ['sale_view.xml'],
    'installable': True,
    'active': False,
}
