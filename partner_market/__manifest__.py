# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Partner Market',
    'version': '0.1',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Adds market field on customers',
    'description': """
Partner Market
==============

This module adds a many2one field *Market* on customers, so be able to have sale/invoicing stats per markets.

We cannot use *Tags* to categorize customers per market because this field is a many2many field, so we cannot make statistics on it.

This module has been written by Alexis de Lattre <alexis.delattre@akretion.com> from Akretion.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'partner_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
