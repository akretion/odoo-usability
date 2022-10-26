# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mail no portal',
    'version': '14.0.1.0.0',
    'category': 'Productivity/Discuss',
    'license': 'AGPL-3',
    'summary': 'Remove portal button in mails sent by Odoo',
    'description': """
This module remove the buttons such as *View Request for Quotation* in emails sent by Odoo.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'maintainers': ['alexis-via'],
    'website': 'https://www.akretion.com',
    'depends': ['mail'],
    'data': [
        'data/mail.xml',
    ],
    'installable': False,
}
