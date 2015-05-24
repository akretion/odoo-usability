# coding: utf-8
##############################################################################
#
#    Copyright 2015 Akretion
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
    'name': 'Product Export Field Profile',
    'version': '1.0',
    'author': 'Akretion',
    'summarize': 'Add predefined list for export',
    'maintainer': 'Akretion',
    'description': """
    Product Export Field Profile
    ============================

    Add export list (native export screen) to:

    * product
    * partner

    Note to mainteners
    ------------------
    You can maintain csv data file and convert in xml
    with https://github.com/akretion/csv2xml4odoo
    """,
    'category': 'product',
    'depends': [
        'product_profile',
    ],
    'website': 'http://www.akretion.com/',
    'data': [
        'misc_data.xml',
        'ir_exports_line_data.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
