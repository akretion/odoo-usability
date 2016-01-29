# -*- coding: utf-8 -*-
##############################################################################
#
#    Web Eradicate Duplicate module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
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
    'name': 'Eradicate Duplicate',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Remove More > Duplicate for all users except admin',
    'description': '''
Eradicate Duplicate
===================

This module is inspired by the module *web_hide_duplicate* of Aristobulo Meneses available on https://github.com/menecio/odoo-addons. The main difference is that it will remove the *More > Duplicate* button everywhere by default for all users except *admin*.

It is possible to restore the duplicate feature on some form views by adding an attribute **duplicate_eradicate="false"** (you will find an example in a comment at the end of the file static/src/js/eradicate_duplicate.js).

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    ''',
    'author': 'Akretion',
    'depends': ['web'],
    'data': ['views/eradicate_duplicate.xml'],
    'installable': True,
}
