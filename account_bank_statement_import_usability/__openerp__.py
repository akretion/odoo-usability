# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Bank Statement Import Usability module for Odoo
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
    'name': 'Account Bank Statement Import Usability',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Small usability enhancements in account_bank_statement_import module',
    'description': """
Account Bank Statement Import Usability
=======================================

This module adds the following changes:

* Blocks the *Automagically create bank account*, because it's too dangerous : it creates new bank accounts and new account journal... and the user doesn't even realize that !

* Works if the bank statement file only contain the account number and not the full IBAN

* If you have 2 accounts with the same number (I know a company that has an account in EUR and an account in USD with the same number), you should force the journal and it will work (instead of blocking with an error message)

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_bank_statement_import'],
    'data': ['account_view.xml'],
    'installable': True,
}
