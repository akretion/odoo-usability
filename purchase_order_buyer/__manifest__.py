# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (https://akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Order Buyer",
    "summary": "Add a buyer (user) on POs",
    "version": "10.0.1.1.0",
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "category": "Purchases",
    "depends": ["purchase"],
    "data": [
        'views/purchase_order.xml',
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
}
