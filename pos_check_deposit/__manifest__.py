# Copyright 2022-2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "POS Check Deposit",
    "version": "18.0.1.0.0",
    "category": "Point of sale",
    "license": "AGPL-3",
    "summary": "Make POS and Check Deposit modules work together",
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "depends": ["point_of_sale"],
    "data": ["views/pos_payment_method.xml"],
    "installable": False,
}
