# -*- coding: utf-8 -*-
##############################################################################
#
#    Mail Usability module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
#    @author Benoît Guillot <benoit.guillot@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Mail Usability',
    'version': '8.0.1.0.0',
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
    'data': ['views/mail.xml'],
    'installable': True,
}
