# -*- coding: utf-8 -*-
# Copyright 2018 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order Full Dropship',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Adds an option full dropship on sale orders',
    'description': """
Sale Order Full Dropship
========================

This module adds a boolean field *Full Dropship* on sale order form. If enabled on a quotation, Odoo will enable the *Dropship* route on all sale order lines of that order. That way, for a full dropship order, the user won't have to open each order line to set the Dropship route.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'sale_stock',
        'stock_dropshipping',
        ],
    'data': [
        'sale_view.xml',
        ],
    'installable': True,
}
