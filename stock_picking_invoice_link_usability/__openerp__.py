# -*- coding: utf-8 -*-
# Copyright (C) 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Stock Picking Invoice Link Usability',
    'version': '8.0.1.0.0',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Small view improvements on stock_picking_invoice_link_usability',
    'description': """
Stock Picking Invoice Link Usability
====================================

I proposed some view modifications for the OCA module stock_picking_invoice_link_usabilityin this PR https://github.com/OCA/stock-logistics-workflow/pull/303  but it was refused, so I decided to develop this additional usability module.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock_picking_invoice_link', 'stock_usability'],
    'data': [
        'stock_view.xml',
        ],
    'installable': True,
}
