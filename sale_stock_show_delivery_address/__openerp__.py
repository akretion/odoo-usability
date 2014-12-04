# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Stock Show Delivery Address module for OpenERP/Odoo
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
    'name': 'Sale Stock Show Delivery Address',
    'version': '0.1',
    'category': '',
    'license': 'AGPL-3',
    'summary': 'Show full address in sale order and delivery order forms',
    'description': """
With this module, you will see the full address in the sale order form view and the delivery order form view.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_stock'],
    'data': ['sale_view.xml', 'stock_view.xml'],
}
