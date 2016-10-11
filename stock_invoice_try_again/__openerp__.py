# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Invoice Try Again module for Odoo
#    Copyright (C) 2013-2015 Akretion (http://www.akretion.com)
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
    'name': 'Stock Invoice Try Again',
    'version': '0.1',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'Add a button to set a picking back to "To Be Invoiced"',
    'description': """
Stock Invoice Try Again
=======================

When the sale order has 'Create Invoice' set to 'On Delivery Order', there is a button 'Create Invoice' on the Delivery Order once the goods are shipped. When the user clicks on this button, OpenERP creates a draft invoice. If the user deletes this draft invoice by mistake, he cannot re-create the invoice. This module is the solution : if the invoice has been deleted, the user can set the picking back to 'To Be Invoiced' and create the invoice again.

Please contact Alexis de Lattre from Akretion <alexis.delattre@akretion.com> for any help or question about this module.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['stock_picking_invoice_link', 'stock_account'],
    'data': ['stock_view.xml'],
    'installable': False,
}
