# -*- encoding: utf-8 -*-
##############################################################################
#
#    POS Journal Sequence module for Odoo
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
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
    'name': 'POS Journal Sequence',
    'version': '0.1',
    'category': 'Point Of Sale',
    'license': 'AGPL-3',
    'summary': 'Order payment buttons in Point of Sale',
    'description': """
This module adds a field *POS Sequence* on account journals that will
allow you to control the order of the payment buttons in the interface
of the point of sale. It requires a patch on the Javascript code of the
point of sale (cf file odoo-point_of_sale.patch).

This module has been written by  Alexis de Lattre
<alexis.delattre@akretion.com>.
    """,
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'depends': ['point_of_sale'],
    'data': ['pos_journal_sequence_view.xml'],
    'installable': True,
}
