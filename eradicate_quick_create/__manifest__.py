# Copyright 2014-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Eradicate Quick Create',
    'version': '12.0.2.0.0',
    'category': 'Tools',
    'license': 'AGPL-3',
    'summary': 'Disable quick create on all objects',
    'description': """
Eradicate Quick Create
======================

Disable quick create on all objects of Odoo.

This new version of the module uses the module *web_m2x_options* from the OCA *web* project instead of the module *base_optional_quick_create* from the OCA project *server-ux*.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['web_m2x_options'],
    'post_init_hook': 'web_m2x_options_create',
    'installable': True,
}
