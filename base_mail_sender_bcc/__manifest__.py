# Copyright 2017-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Mail Sender Bcc',
    'version': '16.0.1.0.3',
    'category': 'Mail',
    'license': 'AGPL-3',
    'summary': "Always send a copy of the mail to the sender",
    'description': """
Mail Sender Bcc
===============

With this module, when Odoo sends an outgoing email, it adds the sender as Bcc (blind copy) of the email.

Examples:

* When a users sends invoice overdue reminders
* When a users sends a Customer Invoice or a Purchase Order

For some other use-cases willingly opt-out, the sender will not be added in Bcc:

* User action triggering fields-tracking message (e.g. validation of a HR Timesheet Sheet)
* Python-submitted message, such as import reports
* Re-routing an inbound email to followers
* message submitted in the chatter to internal users (with an accepted defect: if there is 1 external partner
  within an email mixing both external partners and internal users in recipients, the sender will be added in
  Bcc anyway)
    """,
    'author': 'Akretion',
    'website': 'https://github.com/akretion/odoo-usability',
    'depends': ['mail'],
    'installable': True,
}
