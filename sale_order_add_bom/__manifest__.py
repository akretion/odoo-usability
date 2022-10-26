# Copyright 2016-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Order Add Bom',
    'version': '14.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Wizard to select a bom from a sale order',
    'description': """
This module adds a wizard *Add Kit* on the form view of a quotation that allows the user to select a 'kit' BOM: Odoo will automatically add the components of the kit as sale order lines.

The wizard *Add Kit* is also available on a draft picking.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['sale', 'mrp'],
    'data': [
        'wizard/sale_add_phantom_bom_view.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'security/ir.model.access.csv',
    ],
    'installable': False,
}
