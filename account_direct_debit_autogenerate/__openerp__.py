# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Direct Debit Autogenerate module for Odoo
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
    'name': 'Account Direct Debit Autogenerate',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Auto-generate direct debit order on invoice validation',
    'description': """
Account Direct Debit Autogenerate
=================================

With this module, when you validate a customer invoice whose payment mode is SEPA Direct Debit :

* if a draft Direct Debit order for SEPA Direct Debit already exists, a new payment line is added to it for the invoice,

* otherwise, a new SEPA Direct Debit order is created for this invoice.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_banking_sepa_direct_debit'],
    'data': [],
    'installable': True,
}
