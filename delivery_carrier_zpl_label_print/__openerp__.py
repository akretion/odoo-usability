# -*- coding: utf-8 -*-
##############################################################################
#
#    Delivery Carrier ZPL Label Print module for Odoo
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
    'name': 'Delivery Carrier ZPL Label Print',
    'version': '0.1',
    'category': 'Inventory, Logistic, Storage',
    'license': 'AGPL-3',
    'summary': 'Print ZPL label from delivery order',
    'description': """
Delivery Carrier ZPL Label Print
================================

Add a *Print Label* on Delivery Order that gets the ZPL attached to the picking and sends it to the printer via CUPS.

It requires this PR: https://github.com/OCA/report-print-send/pull/44

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['base_delivery_carrier_label', 'base_report_to_printer'],
    'data': [
        'stock_view.xml',
        'users_view.xml',
        ],
    'installable': True,
}
