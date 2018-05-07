# -*- coding: utf-8 -*-
##############################################################################
#
#    Partner Aged Open Invoices module for Odoo
#    Copyright (C) 2015-2016 Akretion (http://www.akretion.com)
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
    'name': 'Partner Aged Open Invoices',
    'version': '10.0.0.1.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Direct access to the aged open invoice report from the partner form',
    'description': """
Partner Aged Open Invoices
==========================

This module adds a button on the partner form view (the icon on the button is a banknote) to easily open the aged open invoices report of the partner.

It requires the updated version of the module **account_financial_report_webkit** that has the aged open invoice report ; you can find it in this pull request https://github.com/OCA/account-financial-reporting/pull/102

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['account_financial_report_webkit'],
    'data': ['partner_view.xml'],
    'installable': False,
}
