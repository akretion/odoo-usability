# -*- encoding: utf-8 -*-
##############################################################################
#
#    Eradicate Quick Create module for Odoo/OpenERP
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

from openerp.osv import orm


class ir_model(orm.Model):
    _inherit = 'ir.model'

    def init(self, cr):
        '''Activate 'avoid_quick_create' on all existing models'''
        cr.execute(
            "UPDATE ir_model SET avoid_quick_create=true "
            "WHERE avoid_quick_create is not true")
        return True

    _defaults = {
        'avoid_quick_create': True,
    }
