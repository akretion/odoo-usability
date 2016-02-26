# -*- coding: utf-8 -*-
##############################################################################
#
#    Partner Products Shortcut module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
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


# KEEP THIS IN OLD API for the moment
# Otherwise, you will have trouble in the pagination of kanban view and
# the counter for number of records in list view
# Bug found at the Barroux Abbey on 29/5/2015
class ProductTemplate(orm.Model):
    _inherit = 'product.template'

    def search(
            self, cr, uid, args, offset=0, limit=None, order=None,
            context=None, count=False):
        if context is None:
            context = {}
        seller_id = context.get('search_default_seller_id')
        if seller_id:
            seller_ids = self.pool['product.supplierinfo'].search(
                cr, uid, [('name', '=', seller_id)], context=context)
            for argument in args:
                if isinstance(argument, list) and argument[0] == 'seller_ids':
                    args.remove(argument)
            args.append((('seller_ids', 'in', seller_ids)))
        res = super(ProductTemplate, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            count=count, context=context)
        return res
