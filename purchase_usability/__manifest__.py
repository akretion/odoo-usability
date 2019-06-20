# -*- coding: utf-8 -*-
# Copyright (C) 2014-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>


{
    'name': 'Purchase Usability',
    'version': '10.0.0.1.0',
    'category': 'Purchase Management',
    'license': 'AGPL-3',
    'summary': 'Show invoices and receptions on PO',
    'description': """
Purchase Usability Extension
============================

Display Invoices and Incoming Shipments on Purchase Order form view (in dedicated tabs).

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase'],
    'data': [
        'purchase_view.xml',
        'purchase_report.xml',
        'stock_view.xml',
        ],
    'active': False,
}
