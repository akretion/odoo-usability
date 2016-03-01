# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase Suggest module for Odoo
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
    'name': 'Purchase Suggest',
    'version': '0.1',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'summary': 'Suggest POs from special suggest orderpoints',
    'description': """
Purchase Suggest
================

This module is an ALTERNATIVE to the module *procurement_suggest* ; it is similar but it only handles the purchase orders and doesn't generate any procurement : the suggestions create a new purchase order directly.

The advantage is that you are not impacted by the faulty procurements (for example :  a procurement generates a PO ; the PO is confirmed ; the related picking is cancelled and deleted -> the procurements will always stay in running without related stock moves !)

You may want to increase the osv_memory_age_limit (default value = 1h) in Odoo server config file, in order to let some time to the purchase user to finish his work on the purchase suggestions.

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase'],
    'conflicts': ['procurement_suggest'],
    'data': [
        'stock_view.xml',
        'wizard/purchase_suggest_view.xml',
        ],
    'installable': True,
}
