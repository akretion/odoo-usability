# -*- coding: utf-8 -*-
# © 2014-2016 Abbaye du Barroux (http://www.barroux.org)
# © 2016 Akretion (http://www.akretion.com>)
# @author: Frère Bernard <informatique@barroux.org>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Base Partner One2many Phone',
    'version': '10.0.2.0.0',
    'category': 'Phone',
    'license': 'AGPL-3',
    'summary': 'One2many link between partners and phone numbers/emails',
    'description': """
Base Partner One2many Phone
===========================

With this module, one partner can have several phone numbers and several emails. It adds a new table dedicated to phone numbers and emails and a one2many link between partners and phone numbers. This module keeps compatibility with the native behavior of Odoo on phone numbers and emails.

It has been developped by brother Bernard from Barroux Abbey and Alexis de Lattre from Akretion.
    """,
    'author': 'Akretion',
    'website': 'https://akretion.com/',
    'depends': ['base_phone', 'sales_team'],
    'data': [
        'partner_phone_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
    'post_init_hook': 'migrate_to_partner_phone',
}
