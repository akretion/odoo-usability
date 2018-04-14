# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'partner_address_street3 / account_invoice_transmit_method compat.',
    'version': '10.0.0.1.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Compatibility between partner_address_street3 and account_invoice_transmit_method',
    'description': """
Glue module between partner_address_street3 and account_invoice_transmit_method
===============================================================================

Stupid technical module to workaround an Odoo framework limitation about the inherit of the context attribute in a view.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['partner_address_street3', 'account_invoice_transmit_method'],
    'data': [
        'partner_view.xml',
        ],
    'installable': True,
    'auto_install': True,
}
