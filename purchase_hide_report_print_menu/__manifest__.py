# -*- coding: utf-8 -*-
# © 2016 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Hide Report Print Menu',
    'summary': "Hide print report 'Request for Quotation' "
    "in purchase order menu",
    'version': '10.0.1.0.0',
    'category': 'Purchase Management',
    'website': 'http://akretion.com',
    'author': 'Akretion, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'purchase',
    ],
    'data': [
        'purchase_view.xml',
    ]
}
