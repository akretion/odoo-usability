# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase auto invoice method module for OpenERP
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
    'name': 'Purchase Auto Invoice Method',
    'version': '0.1',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'summary': "Set Invoice Method of PO to 'picking', unless if it's service-only",
    'description': """
Purchase Auto Invoice Method
============================

Set the Invoice Method of the Purchase Order to 'picking' by default. On Purchase Order validation, if it only contains service lines, the Invoice Method is automatically switched to 'order'.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase_partner_invoice_method'],
    'data': ['partner_data.xml'],
    'installable': True,
}
