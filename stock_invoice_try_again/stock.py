# -*- encoding: utf-8 -*-
##############################################################################
#
#    Stock Invoice Try Again module for OpenERP
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
from openerp.tools.translate import _


class stock_picking(orm.Model):
    _inherit = 'stock.picking'

    def revert_to_tobeinvoiced(self, cr, uid, ids, context=None):
        assert len(ids) == 1, "Only one picking"
        picking = self.browse(cr, uid, ids[0], context=context)
        if picking.invoice_state == 'invoiced':
            if picking.invoice_id:
                raise orm.except_orm(
                    _('Error:'),
                    _("This picking is linked to the invoice with description '%s'. You should first delete this invoice and try again.")
                    % picking.invoice_id.name)
            self.write(cr, uid, ids[0], {
                'invoice_state': '2binvoiced',
                }, context=context)
        else:
            raise orm.except_orm(
                _('Error:'),
                _("You can only do this when the Delivery Order has 'Invoice State' = 'Invoiced'."))
        return True


class stock_picking_out(orm.Model):
    _inherit = 'stock.picking.out'

    def revert_to_tobeinvoiced(self, cr, uid, ids, context=None):
        return self.pool['stock.picking'].revert_to_tobeinvoiced(
            cr, uid, ids, context=context)


class stock_picking_in(orm.Model):
    _inherit = 'stock.picking.in'

    def revert_to_tobeinvoiced(self, cr, uid, ids, context=None):
        return self.pool['stock.picking'].revert_to_tobeinvoiced(
            cr, uid, ids, context=context)
