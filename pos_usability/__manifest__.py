# Copyright 2014-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "POS Usability",
    "version": "14.0.1.0.0",
    "category": "Point of sale",
    "license": "AGPL-3",
    "summary": "Misc usability improvement for point of sale",
    "description": """
POS Usability
=============

- Sales Details report : add sub total amount by tax


authors
-------

Akretion:

* David Béal <david.beal@akretion.com>

    """,
    "author": "Akretion",
    "website": "http://www.akretion.com",
    "depends": ["point_of_sale"],
    "data": [
        "report/pos.xml",
        "views/pos_category.xml",
        "views/product.xml",
        ],
    "installable": True,
}
