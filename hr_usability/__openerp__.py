# -*- encoding: utf-8 -*-
##############################################################################
#
#    HR Usability module for Odoo
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
    'name': 'HR Usability',
    'version': '0.1',
    'category': 'Human Resources',
    'license': 'AGPL-3',
    'summary': 'Better usability in HR module',
    'description': """
HR Usability
============

The HR module from the official addons adds a field *bank_account_id*. But, if you want to pay an expense note via SEPA Credit Transfer, Odoo doesn't use the bank account of the Employee, but the bank account configured on the Partner. So this module hides this field.

This module has been developped by Alexis de Lattre <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['hr'],
    'data': [
        'hr_view.xml',
        ],
    'installable': True,
}
