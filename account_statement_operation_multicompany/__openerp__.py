# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Statement Operation multi-company module for Odoo
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
    'name': 'Account Statement Operation Multi-company',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Fix multi-company issue on account.statement.operation.template',
    'description': """
This module fixes this bug: https://github.com/odoo/odoo/issues/4706 that OpenERP S.A. didn't want to fix because it requires an update of the datamodel in v8 (I don't think it's a good reason to refuse to fix a bug...).

In v8, the object account.statement.operation.template (corresponds to buttons in the bank statement reconcile interface) doesn't have a company_id field with a record rule. As a consequence, in company A, you see the buttons linked to accounts of company B ! This module fixes this issue.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account'],
    'data': [
        'account_view.xml',
        'security/rule.xml',
        ],
    'installable': True,
}
