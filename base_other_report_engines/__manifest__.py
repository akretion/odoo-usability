# -*- coding: utf-8 -*-
##############################################################################
#
#    Base Other Report Engines module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
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
    'name': 'Base Other Report Engines',
    'version': '0.1',
    'category': '',
    'license': 'AGPL-3',
    'summary': 'Allows the use of report engines other than Qweb',
    'description': """
Base Other Report Engines
=========================

This module inherit the method *_get_report_from_name()* to allow the use of report engines other than Qweb.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['report'],
    'data': [],
}
