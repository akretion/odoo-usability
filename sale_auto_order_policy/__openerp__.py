# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Auto Order Policy module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
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
    'name': 'Sale Auto Order Policy',
    'version': '0.1',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': "Order Policy = 'On Delivery Order' by default, switches to 'On Demand' when service-only",
    'description': """
Sale Auto Order Policy
======================

With this module, the Order Policy on Quotations is set to 'On Delivery Order' by default. If the Quotation only contains service lines, the Order Policy is switched to 'On Demand' when the Quotation is confirmed.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale', 'stock'],
    'data': [],
    'images': [],
    'installable': True,
    'active': False,
}
