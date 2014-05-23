# -*- encoding: utf-8 -*-
##############################################################################
#
#    Asterisk click2dial Project Issue module for OpenERP
#    Copyright (c) 2014 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
    "name": "Asterisk Click2dial Project Issue",
    "version": "0.1",
    "author": "Akretion",
    "website": "http://www.akretion.com",
    "license" : "AGPL-3",
    "category": "Project Management",
    "description": """
    This module adds a button "Open Related Issues" on the "Open calling partner" wizard.

    A detailed documentation for the OpenERP-Asterisk connector is available on the Akretion Web site : http://www.akretion.com/open-source-contributions/openerp-asterisk-voip-connector
    """,
    "depends": [
        'asterisk_click2dial',
        'project_issue',
    ],
    "demo": [],
    "data": [
        'wizard/open_calling_partner_view.xml',
    ],
    "installable": True,
}
