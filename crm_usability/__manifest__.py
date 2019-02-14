# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'CRM Usability',
    'version': '10.0.1.0.0',
    'category': 'Customer Relationship Management',
    'license': 'AGPL-3',
    'summary': 'CRM usability enhancements',
    'description': """
CRM Usability
=============

Some enhancements in the *Merge Partners* wizard:

* take into account the unaccent option of the server config file
* add optional group by on 'customer' and 'supplier' (active by default)

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['crm'],
    'data': [
        #'wizard/base_partner_merge_view.xml',
        'security/crm_security.xml',
        'crm_view.xml',
        ],
    'installable': True,
}
