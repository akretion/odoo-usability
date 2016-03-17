# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Date Planned Update module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#    @author Sébastien Beau <sebastien.beau@akretion.com>
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
from openerp import SUPERUSER_ID


class PurchaseOrderLine(orm.Model):
    _inherit = 'purchase.order.line'

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('date_planned'):
            if not isinstance(ids, list):
                ids = [ids]
            polines = self.browse(cr, uid, ids, context=context)
            move_ids = []
            for poline in polines:
                # Add msg in chatter
                poline.order_id.message_post(_(
                    "Updated Scheduled Date of line <b>%s</b> from %s "
                    "to <b>%s</b>"
                    % (poline.name, poline.date_planned,
                       vals['date_planned'])))
                move_ids += [
                    sm.id for sm in poline.move_ids if sm.state != 'done']
            if move_ids:
                # update related stock move
                self.pool['stock.move'].write(cr, SUPERUSER_ID, move_ids, {
                    'date_expected': vals['date_planned'],
                    }, context=context)
        return super(PurchaseOrderLine, self).write(
            cr, uid, ids, vals, context=context)
