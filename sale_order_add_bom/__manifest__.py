# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order Add Bom',
    'version': '10.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Wizard to select a bom from a sale order',
    'description': """
This module adds a wizard *Add Kit* on the form view of a quotation that allows the user to select a 'kit' BOM: Odoo will automatically add the components of the kit as sale order lines.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['sale', 'mrp'],
    'data': [
        'wizard/sale_add_phantom_bom_view.xml',
        'sale_view.xml',
    ],
    'installable': True,
}
