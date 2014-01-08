# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Auto Order Policy module for OpenERP
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


class sale_order(orm.Model):
    _inherit = 'sale.order'

    _defaults = {
        'order_policy': 'picking',
    }

    def action_button_confirm(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only one ID'
        so = self.browse(cr, uid, ids[0], context=context)
        service_only = True
        for line in so.order_line:
            if line.product_id and line.product_id.type != 'service':
                service_only = False
        if service_only:
            so.write({'order_policy': 'manual'})
        return super(sale_order, self).action_button_confirm(
            cr, uid, ids, context=context)
