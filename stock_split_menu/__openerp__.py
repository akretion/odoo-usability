# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Split Menu",
    "summary": "Split the receive, internal move, ship menu",
    "version": "8.0.1.0.0",
    "category": "Warehouse",
    "website": "www.akretion.com",
    "author": " Akretion",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "stock",
    ],
    "data": [
        "view/stock_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
