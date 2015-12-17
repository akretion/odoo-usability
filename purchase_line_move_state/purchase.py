# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Line Move State module for Odoo
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

from openerp.osv import orm, fields
from openerp.tools.translate import _


class PurchaseOrderLine(orm.Model):
    _inherit = 'purchase.order.line'

    def _get_reception_state(
            self, cr, uid, ids, field_name, args, context=None):
        res = {}
        state_label = {
            'assigned': _('Waiting'),
            'done': _('Received'),
            'cancel': _('Cancelled'),
            }
        for line in self.browse(cr, uid, ids, context=context):
            count = {}
            for move in line.move_ids:
                if move.state in count:
                    count[move.state] += move.product_qty
                else:
                    count[move.state] = move.product_qty
            if count:
                entries = []
                for state, qty in count.iteritems():
                    entries.append(
                        "%s: %s" % (state_label.get(state, state), qty))
                label = "\n".join(entries)
            else:
                label = _('Not applicable')
            res[line.id] = label
        return res

    _columns = {
        'reception_state': fields.function(
            _get_reception_state,
            string='Reception Status', readonly=True,
            type='char', help="Human readable status of the reception."),
        }
