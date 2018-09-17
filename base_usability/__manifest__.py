# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Usability',
    'version': '10.0.0.1.0',
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

It displays the local modules with installable filter.
A group by 'State' is added to module search view.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'partner_view.xml',
        'partner_bank_view.xml',
        'users_view.xml',
        'country_view.xml',
        'module_view.xml',
        ],
    'installable': True,
}
