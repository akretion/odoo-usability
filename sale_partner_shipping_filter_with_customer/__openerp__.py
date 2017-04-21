# coding: utf-8
# © 2017 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Partner Shipping Filter with Customer',
    'summary': "Shows only delivery addresses that are linked "
    "with the customer",
    'version': '8.0.1.0.0',
    'category': 'Sale Management',
    'website': 'http://akretion.com',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_view.xml',
    ]
}
