# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Markup Group User module for OpenERP
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
    'name': 'Sale Markup Group User',
    'version': '0.1',
    'category': 'Sales Management',
    'license': 'AGPL-3',
    'summary': "Margins and markups shouldn't be visible only to the Sale Manager",
    'description': """
Sale Markup Group User
======================

As discussed in this bug report https://bugs.launchpad.net/sale-financial/+bug/1305987, I think that the fields added by the sale_markup module should be visible to Sale Users, not only to Sale Managers.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_markup'],
    'data': ['sale_view.xml'],
    'installable': True,
    'active': False,
}
