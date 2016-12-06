# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Product Shortcut',
    'version': '10.0.1.0.0',
    'category': 'Contact Management',
    'license': 'AGPL-3',
    'summary': 'Adds a shortcut on partner form to the products supplied by this partner',
    'description': """
Partner Product Shortcut
========================

Adds a shortcut on supplier partner form to the products supplied by this partner (display the product variants view).

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
    'data': ['partner_view.xml'],
    'installable': True,
}
