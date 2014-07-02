# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner Products Shortcut module for OpenERP
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


class res_partner(orm.Model):
    _inherit = 'res.partner'

    def _product_supplied_count(
            self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x, 0), ids))
        try:
            for partner_id in ids:
                seller_ids = self.pool['product.supplierinfo'].search(
                    cr, uid, [('name', '=', partner_id)], context=context)
                pt_ids = self.pool['product.template'].search(
                    cr, uid, [('seller_ids', 'in', seller_ids)],
                    context=context)
                res[partner_id] = len(pt_ids)
        except:
            pass
        return res

    _columns = {
        'product_supplied_count': fields.function(
            _product_supplied_count, string="# of Products Supplied",
            type='integer'),
        }
