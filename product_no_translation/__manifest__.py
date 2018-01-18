# -*- coding: utf-8 -*-
# © 2014-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Product no Translation',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': "For companies work with several languages but not for products",
    'description': """
This module sets the translatable fields of the product object (name,
descriptions) to non-translatable fields.

This change is usefull for companies that work with several languages BUT that don't translate product names.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['product'],
}
