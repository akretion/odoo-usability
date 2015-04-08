# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 EduSense BV (<http://www.edusense.nl>).
#              (C) 2011 - 2013 Therp BV (<http://therp.nl>).
#              (C) 2014 ACSONE SA/NV (<http://acsone.eu>).
#
#    All other contributions are (C) by their respective contributors
#
#    All Rights Reserved
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
    'name': 'Account Banking - Payments Transfer Account (simple)',
    'version': '0.2',
    'license': 'AGPL-3',
    'author': "Akretion,Odoo Community Association (OCA)",
    'website': 'http://www.akretion.com',
    'category': 'Banking addons',
    'depends': [
        'account_banking_payment_export',
    ],
    'data': [
        'view/payment_mode.xml',
        'workflow/account_payment_workflow.xml',
    ],
    'description': '''
This is a simple equivalent for Odoo v7 of the module *account_banking_payment_transfer* for v8.0.

I developped this module to be able to make some SEPA direct debits / credit transfer with transfer move on Odoo v7, without installing the module account_banking (I can't install account_banking because I used the OCA modules from https://github.com/OCA/bank-statement-reconcile)
    ''',
    'installable': True,
}
