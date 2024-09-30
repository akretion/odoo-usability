# Copyright 2014-2024 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Product Shortcut',
    'version': '16.0.1.0.0',
    'category': 'Contact Management',
    'license': 'AGPL-3',
    'summary': 'Adds a shortcut on partner form to the products supplied by this partner',
    'description': """
Partner Product Shortcut
========================

Adds a smartbutton on partner form to the products supplied by this partner.

This is an alternative to the OCA module `partner_supplierinfo_smartbutton <https://github.com/OCA/purchase-workflow/tree/14.0/partner_supplierinfo_smartbutton>`_ which adds a smartbutton on partner form to links to the related product.supplierinfo (and not to product.template like in this module).

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['product'],
    'data': ['res_partner_view.xml'],
    'installable': True,
}
