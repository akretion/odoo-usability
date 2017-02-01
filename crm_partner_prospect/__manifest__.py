# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'CRM Partner Prospect',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': "Glue module between base_partner_prospect and crm modules",
    'description': """
CRM Partner Prospect
=====================

This is a glue module between *base_partner_prospect* and *crm* modules.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['crm', 'base_partner_prospect'],
    'data': [
        'crm_view.xml',
        ],
    'installable': True,
    'auto_install': True,
}
