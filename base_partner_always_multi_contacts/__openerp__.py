# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Partner Always Multi Contacts module for OpenERP
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
    'name': 'Base Partner Always Multi Contacts',
    'version': '0.1',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Both individuals and companies can have multiple contacts',
    'description': """
Base Partner Always Multi Contacts
==================================

By default, you can't enter several addresses for an individual in OpenERP because thee "Contacts" tab is hidden when the field *is Company* is not active. This module solves this.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': ['partner_view.xml'],
    'installable': True,
    'active': False,
}
