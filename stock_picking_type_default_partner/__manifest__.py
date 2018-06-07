# -*- coding: utf-8 -*-
# Copyright (C) 2014-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Stock Picking Type Default Partner',
    'version': '10.0.1.0.0',
    'category': 'Inventory, Logistics, Warehousing',
    'license': 'AGPL-3',
    'summary': 'Adds a default partner on types of operation',
    'description': """
Stock Picking Type Default Partner
==================================

This module adds a new field on the Types of Operation (stock.picking.type) : *Default Partner*. This is useful for multi-site companies that create inter-site Type of Operations: all the operations that use this Type of Operation should have the same destination partner.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock'],
    'data': ['stock_view.xml'],
    'installable': True,
}
