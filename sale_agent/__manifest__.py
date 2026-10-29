# Copyright 2024 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale Agent',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'license': 'AGPL-3',
    'summary': 'Add agent on partner, sale order and customer invoice/refund',
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['sale'],
    'data': [
        "views/res_partner.xml",
        "views/sale_order.xml",
        "views/sale_report.xml",
        "views/account_move.xml",
        "views/account_invoice_report.xml",
        ],
    'demo': ['demo/demo.xml'],
    'installable': False,
}
