# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale no optional product",
    "summary": "Hide optional product",
    "version": "12.0.1.0.0",
    "category": "Usability",
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
        "sale_management",
    ],
    "data": [
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
