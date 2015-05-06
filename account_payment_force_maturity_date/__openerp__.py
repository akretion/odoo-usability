# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Payment Force Maturity Date module for Odoo
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
    'name': 'Account Payment Force Maturity Date',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Add a Force Maturity Date field on payment lines',
    'description': """
Account Payment Force Maturity Date
===================================

This module adds a field *Force Maturity Date* on payment lines. If this field is set, the maturity date of the payment line will take the value of this field instead of taking the value of the maturity date of the related account move line.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
""",
    'author': 'Akretion',
    'depends': ['account_payment'],
    'data': ['payment_view.xml'],
}
