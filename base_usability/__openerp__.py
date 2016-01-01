# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Usability module for Odoo
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
    'name': 'Base Usability',
    'version': '0.1',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Better usability in base module',
    'description': """
Base Usability
==============

This module adds *track_visibility='onchange'* on all the important fields of the Partner object.

By default, Odoo doesn't display the title field on all the partner form views. This module fixes it (it replaces the module base_title_on_partner).

By default, users in the Partner Contact group also have create/write access on Countries and States. This module removes that: only the users in the *Administration > Configuration* group have create/write/delete access on those objects.

It also adds a log message at INFO level when sending an email via SMTP.

It displays the Local modules by default in tree view (instead of Kanban) filtered on installed modules (instead of filtered on Apps).
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base', 'mail'],
    'data': [
        'partner_view.xml',
        'country_view.xml',
        'module_view.xml',
        'translation_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
