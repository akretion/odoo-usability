# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "POS Check Deposit",
    "version": "16.0.1.0.0",
    "category": "Point of sale",
    "license": "AGPL-3",
    "summary": "Make POS and Check Deposit module work together",
    "description": """
POS Check Deposit
=================

On POS payment method, there is a boolean field named 'split_transactions' which has a string "Identify Customer". When this option is enabled, the payment move lines are split (which is required for the account_check_deposit module) and you must select a Customer on the POS order (which is not really needed for a payment by check).

The goal of this module is to have 2 different options on POS payment method:

* split_transactions (the current field), to split the payment move lines
* identify_customer (a new field), to require the selection of a customer on the POS order

That way, you can configure the **Check** payment method with split_transactions enabled and identify_customer disabled.

WARNING: this module requires a patch on the point_of_sale module. The patch is available in the root directory of the module under the name **odoo-pos_check_deposit.diff**.

Authors
-------

Akretion:

* Alexis de Lattre <alexis.delattre@akretion.com>

    """,
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_payment_method.xml",
        ],
    "installable": True,
}
