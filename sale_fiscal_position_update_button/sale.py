# -*- coding: utf-8 -*-
#############################################################################
#
#    Sale Fiscal Position Update module for OpenERP
#    Copyright (C) 2011-2014 Julius Network Solutions SARL <contact@julius.fr>
#    Copyright (C) 2014 Akretion (http://www.akretion.com)
#    @author Mathieu Vatel <mathieu _at_ julius.fr>
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
from openerp.tools.translate import _


class sale_order(orm.Model):
    _inherit = "sale.order"

    def update_fiscal_position(self, cr, uid, ids, context=None):
        '''Function executed by the "(update)" button on orders
        If the orders are in draft state, it updates taxes and accounts
        on all order lines'''
        fp_obj = self.pool['account.fiscal.position']
        for order in self.browse(cr, uid, ids, context=context):
            if order.state not in ('sent', 'draft'):
                raise orm.except_orm(
                    _('Error:'),
                    _('You cannot update the fiscal position because the '
                        'sale order is not in draft or sent state.'))
            fp = order.fiscal_position
            for line in order.order_line:
                if line.product_id:
                    product = self.pool['product.product'].browse(
                        cr, uid, line.product_id.id, context=context)
                    taxes = product.taxes_id
                    tax_ids = fp_obj.map_tax(
                        cr, uid, fp, taxes, context=context)
                    line.write({'tax_id': [(6, 0, tax_ids)]}, context=context)
                else:
                    raise orm.except_orm(
                        _('Error:'),
                        _("Cannot update the fiscal position because "
                            "the line '%s' doesn't have a product.")
                        % line.name)
        return True
