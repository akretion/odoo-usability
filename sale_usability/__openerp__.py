# -*- coding: utf-8 -*-
##############################################################################
#
#    Sale Usability module for Odoo
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
    'name': 'Sale Usability',
    'version': '0.1',
    'category': 'Sale Management',
    'license': 'AGPL-3',
    'summary': 'Show invoices on sale orders',
    'description': """
Sale Usability Extension
========================

Several small usability improvements:

* Display Invoices on Sale Order form view (in dedicated tab).
* Display currency in tree view

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': [
        'sale_view.xml',
        ],
    'installable': True,
}
