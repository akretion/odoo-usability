# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Layout Category Product',
    'version': '10.0.1.0.0',
    'category': 'Sale Management',
    'license': 'AGPL-3',
    'summary': 'Assign a default sale layout category on products',
    'description': """
Sale Layout Category on Products
================================

With this module, you can configure a default sale layout category on products (product.template).

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': ['product_view.xml'],
    'installable': True,
}
