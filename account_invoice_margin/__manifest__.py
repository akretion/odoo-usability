# -*- coding: utf-8 -*-
# © 2015-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>

{
    'name': 'Account Invoice Margin',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Copy standard price on invoice line and compute margins',
    'description': """
This module copies the field *standard_price* of the product on the invoice line when the invoice line is created. The allows the computation of the margin of the invoice.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'data': [
        'account_invoice_view.xml',
    ],
    'installable': True,
}
