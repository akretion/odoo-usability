# Copyright 2014-2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "POS Usability",
    "version": "18.0.1.0.0",
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
    "website": "https://github.com/akretion/odoo-usability",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        # "report/pos.xml",  # TODO mig if needed
        "views/report_pos_order.xml",
        "views/pos_category.xml",
        "views/pos_session.xml",
        "views/pos_payment_method.xml",
        "views/pos_order.xml",
        ],
    "installable": True,
}
