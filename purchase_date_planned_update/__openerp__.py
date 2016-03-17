# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Date Planned Update module for Odoo
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
    'name': 'Purchase Date Planned Update',
    'version': '0.1',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'summary': "Update of date planned on PO line updates date on stock move",
    'description': """
Purchase Date Planned Update
============================

This module adds a wizard on confirmed purchase orders to update the date planned on one or several purchase order lines: it will update the scheduled date of the purchase order lines and the expected date of the related stock moves that are not already received.

This module has been written by Alexis de Lattre from Akretion
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase'],
    'data': [
        'wizard/purchase_date_planned_update_view.xml',
        'purchase_view.xml',
        ],
    'installable': True,
}
