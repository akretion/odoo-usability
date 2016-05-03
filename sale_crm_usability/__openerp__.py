# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Sale CRM Usability',
    'version': '8.0.1.0.0',
    'category': 'Customer Relationship Management',
    'license': 'AGPL-3',
    'summary': 'Link between opportunities and sale orders',
    'description': """
Sale CRM Usability
==================

This module adds a One2many link from opportunities to sale orders.

When a sale order linked to an opportunity is confirmed, the opportunity
is automatically moved to the *Won* step.

When you click on the button *Mark as lost* on an opportunity, the related quotations (*draft* or *sent* state) are automatically cancelled.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale_crm'],
    'data': ['sale_crm_view.xml'],
    'installable': True,
}
