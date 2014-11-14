# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Tracking UL module for OpenERP
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

from openerp.osv import orm, fields


class product_ul(orm.Model):
    _inherit = 'product.ul'

    _columns = {
        # These fields are backported from Odoo v8
        # In v8, they don't say what is the unit of measure !!!
        # so I suppose it is cm and kg
        'height': fields.float('Height (cm)', help='The height of the package in cm'),
        'width': fields.float('Width (cm)', help='The width of the package in cm'),
        'length': fields.float('Length (cm)', help='The length of the package in cm'),
        'weight': fields.float('Empty Package Weight (kg)'),
        }
