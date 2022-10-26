# Copyright 2021 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Shopinvader Usability",
    "description": """
        Shopinvader Usability""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "https://github.com/OCA/odoo-usability",
    "depends": [
        "shopinvader",
        "sale_usability",
    ],
    "data": ["views/sale_views.xml"],
    "installable": False,
    "auto_install": True,
}
