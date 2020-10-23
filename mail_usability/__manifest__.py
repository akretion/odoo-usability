# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author Benoît Guillot <benoit.guillot@akretion.com>
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mail Usability',
    'version': '10.0.1.0.0',
    'category': 'Base',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on mails',
    'description': """
Mail Usability
==============

Small usability improvements on mails:

* remove link in mail footer

* remove 'sent by' in notification footer

* add a new entry *All Messages Except Notifications* to the field *Receive Inbox Notifications by Email* of partners (becomes the default value)
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mail'],
    'data': [
        'views/mail_view.xml',
        'data/mail_data.xml',
        'wizard/email_template_preview_view.xml',
        'wizard/mail_compose_message_view.xml',
        ],
    'installable': True,
}
