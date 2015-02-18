# -*- encoding: utf-8 -*-
##############################################################################
#
#    POS Sale Report module for Odoo
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
    'name': 'POS Sale Report',
    'version': '0.1',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': 'Add a graph via on that aggregate sale orders and pos orders',
    'description': """
In the *Reporting* menu, add a new entry *POS + Sale Orders Analysis* that show sale statistics per products that aggregate sale orders and pos orders.

Also add direct access to Sales statistics on the Product form view and Product Variants form view (Menu entry *Sales Statistics* in the *More* drop down list).

This module has been written by  Alexis de Lattre
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale', 'sale'],
    'data': [
        'report/pos_sale_report_view.xml',
        'product_view.xml',
        'security/ir.model.access.csv',
        ],
    'installable': True,
}
