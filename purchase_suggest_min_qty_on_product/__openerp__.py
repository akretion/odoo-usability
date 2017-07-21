# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Suggest Min Qty on Product module for Odoo
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
    'name': 'Purchase Suggest Min Qty on Product',
    'version': '0.1',
    'category': 'Purchase',
    'license': 'AGPL-3',
    'summary': 'Replace orderpoints by a min_qty field on product',
    'description': """
Purchase Suggest Min Qty on Product
===================================

With this module, instead of using orderpoints, we add a *min_qty* field on product.product and we use this value as the minimum stock. This makes it easier for users to read and update the min_qty. But this should only be used if there is only 1 warehouse where we handle min stock rules (because, with this module, you cannot set min_qty per warehouse or per stock location).

This module has been written by Alexis de Lattre from Akretion <alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['purchase_suggest'],
    'data': [
        'product_view.xml',
        'wizard/purchase_suggest_view.xml',
        ],
    'installable': False,
}
