# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner Default Lang Parent module for OpenERP
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
    'name': 'Partner Default Lang Parent',
    'version': '0.1',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'A new contact gets the language of the parent by default',
    'description': """
By default, if you create a new contact on a company form, this new contact will have the language of the user that create it. This module changes this behavior : a contact now gets the language of it's parent company by default.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': ['partner_view.xml'],
    'installable': True,
}
