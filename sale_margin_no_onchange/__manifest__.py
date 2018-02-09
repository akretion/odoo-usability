# -*- coding: utf-8 -*-
# Copyright (C) 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    'name': 'Sale Margin No Onchange',
    'version': '10.0.1.0.0',
    'category': 'Accounting',
    'license': 'AGPL-3',
    'summary': 'Copy standard price on sale order line and compute margins',
    'description': """
This module copies the field *standard_price* of the product on the sale order line when the sale order line is created. The allows the computation of the margin of the sale order.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale'],
    'data': [
        'sale_view.xml',
    ],
    'installable': True,
}
