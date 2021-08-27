# Copyright 2016-2021 Akretion France (http://www.akretion.com)
# @author Benoît Guillot <benoit.guillot@akretion.com>
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mail Usability',
    'version': '14.0.1.0.0',
    'category': 'Productivity/Discuss',
    'license': 'AGPL-3',
    'summary': 'Usability improvements on mails',
    'description': """
Mail Usability
==============

Small usability improvements on mails:

* remove link in mail footer (TODO mig v14)

* remove 'sent by' in notification footer (TODO mig v14)
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['mail'],
    'data': [
        #'views/mail_view.xml',
        #'data/mail_data.xml',
        #'wizard/email_template_preview_view.xml',
        #'wizard/mail_compose_message_view.xml',
        ],
    'installable': True,
}
