# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase Auto Invoice Method module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
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


class purchase_order(orm.Model):
    _inherit = 'purchase.order'

    _defaults = {
        'invoice_method': 'picking',
    }

    def wkf_confirm_order(self, cr, uid, ids, context=None):
        invoice_method_order_po_ids = []
        for po in self.browse(cr, uid, ids, context=context):
            if all([l.product_id.type == 'service' for l in po.order_line]):
                invoice_method_order_po_ids.append(po.id)
        if invoice_method_order_po_ids:
            self.write(cr, uid, invoice_method_order_po_ids, {
                'invoice_method': 'order',
                }, context=context)
        res = super(purchase_order, self).wkf_confirm_order(
            cr, uid, ids, context=context)
        return res
