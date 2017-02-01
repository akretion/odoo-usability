# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Partner Prospect',
    'version': '10.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': "Add boolean field 'Prospect' on partners",
    'description': """
Base Partner Prospect
=====================

This module adds a regular boolean field *Prospect* on partner form view.

This module is a different implementation of the OCA module *partner_prospect* which adds the same field on partners: that module doesn't use a regular boolean field but a compute boolean field. I don't like this approch because I want to have manual control over that field and have a customer with prospect = False even if there is not sale order in Odoo for that customer.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base'],
    'data': [
        'partner_view.xml',
        ],
    'installable': True,
}
