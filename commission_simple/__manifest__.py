# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Commission Simple',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Compute commissions for salesman',
    'description': """
Commission Simple
=================

This module is a **simple** module to compute commission for salesman. From my experience, companies often use very specific methods to compute commissions and it's impossible to develop a module that can support all of them. So the goal of this module is just to have a simple base to build the company-specific commissionning system by inheriting this simple module.

Here is a short description of this module:

* create commission profiles using rules (per product category, per product, per product and customer, etc.),
* the commission rules can have a start and end date (optional),
* commissionning can happen on invoicing or on payment,
* each invoice line can only be commissionned to one salesman,
* commission reports are stored in Odoo.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': [
        'account',
        'date_range',
        # this uses some related fields on account.invoice.line
        'account_usability',
        ],
    'data': [
        'data/decimal_precision.xml',
        'views/commission.xml',
        'views/res_users.xml',
        'views/account_config_settings.xml',
        'wizard/commission_compute_view.xml',
        'security/ir.model.access.csv',
        'security/rule.xml',
        ],
    'installable': True,
}
