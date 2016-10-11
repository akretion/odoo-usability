# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Stock Usability module for Odoo
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
    'name': 'Sale Stock Usability',
    'version': '0.2',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': 'Small usability improvements to the sale_stock module',
    'description': """
Sale Stock Usability
====================

The usability enhancements include:

* *To invoice* filter on pickings filters on invoice_state = 2binvoiced AND state = done
* Add a tab with the list of related pickings in sale order form

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_stock'],
    'data': ['sale_stock_view.xml'],
    'installable': False,
}
