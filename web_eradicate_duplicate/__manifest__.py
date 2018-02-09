# -*- coding: utf-8 -*-
#  Copyright (C) 2016-2018 Akretion (http://www.akretion.com)
#  @author Alexis de Lattre <alexis.delattre@akretion.com>
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Eradicate Duplicate',
    'version': '10.0.1.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Remove Action > Duplicate for all users except admin',
    'description': '''
Eradicate Duplicate
===================

This module is inspired by the module *web_hide_duplicate* of Aristobulo Meneses available on https://github.com/menecio/odoo-addons (it seems this URL doesn't exist any more, so I don't know where the module is located now). The main difference is that it will remove the *Action > Duplicate* button everywhere by default for all users except *admin*.

It is possible to restore the duplicate feature on some form views by adding an attribute **duplicate_eradicate="false"** (you will find an example in a comment at the end of the file static/src/js/eradicate_duplicate.js).

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    ''',
    'author': 'Akretion',
    'depends': ['web'],
    'data': ['views/eradicate_duplicate.xml'],
    'installable': True,
}
