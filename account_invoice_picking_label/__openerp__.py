# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Invoice Picking Label module for OpenERP
#    Copyright (C) 2014 Akretion
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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
    'name': 'Account Invoice Picking Label',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Adds field picking_ids_label on account.invoice',
    'description': """
Account Invoice Picking Label
=============================

Adds a function field named *picking_ids_label* on invoices. This field contains the list of pickings related to the invoice as a string. This field is designed to be displayed in the invoice report.""",
    'author': 'Akretion',
    'website': 'http://www.akretion.com/',
    'depends': ['stock_picking_invoice_link'],
    'installable': True,
}
