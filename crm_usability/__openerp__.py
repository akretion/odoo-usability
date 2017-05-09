# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'CRM Usability',
    'version': '8.0.1.0.1',
    'category': 'Customer Relationship Management',
    'license': 'AGPL-3',
    'summary': 'CRM usability enhancements',
    'description': """
CRM Usability
=============

The usability improvements include :

* Adds multi-company record rules on crm.lead.
* Some enhancements in the *Merge Partners* wizard:
  * take into account the unaccent option of the server config file
  * add optional group by on 'customer' and 'supplier' (active by default)

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['crm'],
    'data': [
        'crm_view.xml',
        'wizard/base_partner_merge_view.xml',
        'security/rule.xml',
        ],
    'installable': True,
}
