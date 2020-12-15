# Copyright 2016-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Partner Tree Default - Contacts',
    'version': '14.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Tree view by default instead of kanban for partners',
    'description': """
Partner Tree Default - Contacts
===============================

With this module, when you select a *Customer* or *Vendors* menu entry, you will see the list view by default instead of the kanban view.

This module has been written by Alexis de Lattre <alexis.delattre@akretion.com> from Akretion.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['contacts'],
    'data': ['views/res_partner.xml'],
    'installable': True,
}
