# Copyright 2021 Akretion (https://www.akretion.com).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Stock relation usability",
    "summary": "SUMMARY",
    "version": "14.0.1.0.0",
    "category": "Inventory, Logistic, Storage",
    "website": "http://www.akretion.com",
    "author": "Akretion",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "stock",
        "purchase",
    ],
    "data": [
        "views/stock_picking.xml",
    ],
    "demo": [],
    "qweb": [],
}
