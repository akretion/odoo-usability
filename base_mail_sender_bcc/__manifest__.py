# Copyright 2017-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mail Sender Bcc',
    'version': '14.0.1.0.0',
    'category': 'Mail',
    'license': 'AGPL-3',
    'summary': "Always send a copy of the mail to the sender",
    'description': """
Mail Sender Bcc
===============

With this module, when Odoo sends an outgoing email, it adds the sender as Bcc (blind copy) of the email.
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['base'],
    'installable': True,
}
