# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Del Attachment Cancel module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'Account Invoice Delete Attachment on Cancel',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Delete the attachment on the invoice when it is set back to draft',
    'description': """
Account Invoice Delete Attachment on Cancel
===========================================

When a customer invoice is validated, on the first generation of the invoice report, a copy of the report is stored as attachment on the invoice. After that, every time a user asks for the Invoice report, it will be taken from the attachment. But, when a customer invoice/refund is cancelled, set back to draft, modified and re-validated, the Invoice report is still the old PDF file, which is often raised as a bug by the users.

With this module, when a customer invoice/refund is set back to draft, the attachment is deleted.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'installable': True,
}
