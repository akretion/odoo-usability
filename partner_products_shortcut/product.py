# -*- encoding: utf-8 -*-
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

from openerp import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def search(
            self, args, offset=0, limit=None, order=None, count=False):
        seller_id = self.env.context.get('search_default_seller_id')
        if seller_id:
            sellers = self.env['product.supplierinfo'].search(
                [('name', '=', seller_id)])
            for argument in args:
                if isinstance(argument, list) and argument[0] == 'seller_ids':
                    args.remove(argument)
            args.append((('seller_ids', 'in', sellers.ids)))
        return super(ProductTemplate, self).search(
            args, offset=offset, limit=limit, order=order, count=count)
