# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Delivery Usability',
    'version': '10.0.1.0.0',
    'category': 'Stock',
    'license': 'AGPL-3',
    'summary': 'Several usability enhancements in Delivery',
    'description': """
Delivery Usability
===================

The usability enhancements include:
* display product_id in form view of delivery.carrier (allows to create a delivery carrier from a pre-existing product)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['delivery'],
    'data': [
        'delivery_view.xml',
        ],
    'installable': True,
}
