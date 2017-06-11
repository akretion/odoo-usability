# -*- encoding: utf-8 -*-
##############################################################################
#
#    Project Issue Extension module for OpenERP
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
    'name': 'Project Issue Extension',
    'version': '10.0.0.1.0',
    'category': 'Project Management',
    'license': 'AGPL-3',
    'summary': 'Better usability for Project Issues',
    'description': """
Project Issue Extension
=======================

This module adds 3 fields on project issues :

* a *Number* field, attached to a sequence (replaces the "ID"),

* a *Target Resolution Date* (datetime),

* a *Related Products* fields (many2many).

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['project_issue'],
    'data': [
        'project_view.xml',
        'project_data.xml',
        ],
    'active': False,
}
