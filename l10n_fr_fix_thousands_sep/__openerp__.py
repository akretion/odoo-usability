# -*- coding: utf-8 -*-
##############################################################################
#
#    L10n FR Fix Thousands Separator module for Odoo
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
    'name': 'L10n FR Fix Thousands Separator',
    'version': '8.0.0.1.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Thousands separator of fr_FR updated to Narrow No-Break Space',
    'description': """
L10n FR Fix Thousands Separator
===============================

Make sure that the language fr_FR is installed **before** installing this module.

By default, the French language (fr_FR) has space as *Thousands Separator* and the *Separator Format* is not set. If you manually set a good value for *Separator Format* ([3,0]) and you keep space as *Thousands Separator*, you will get the following problem: when you display a float with a value over one thousand and there isn't enough horizontal space in the tree or form view, the number will be displayed over 2 lines (or more). This often happens in *Accounting > Journal Entries > Journal Items* for users that don't have super-wide screens. And it is a cause of headache for accountants ! :)

When you install this module:

* on language with code *fr_FR*, the Thousands Separator* will be set to the unicode caracter U+202F *NARROW NO-BREAK SPACE* (http://www.fileformat.info/info/unicode/char/202f/index.htm) and the *Separator Format* will be set to [3,0].

* on language with code *en_US* (installed by default), the *Separator Format* will be set to [3,0].

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': "Akretion",
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'installable': True,
}
