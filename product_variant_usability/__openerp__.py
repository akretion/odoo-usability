# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Variant Usability",
    "summary": "Improve the product variant usability",
    "version": "8.0.1.0.0",
    "category": "Uncategorized",
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
        "product_variant_inactive",
    ],
    "data": [
        "views/product_view.xml",
        "views/product_attribute_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
