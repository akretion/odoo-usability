# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Invoice Picking Label module for OpenERP
#    Copyright (C) 2013-2014 Akretion
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    def _compute_picking_ids_label(
            self, cr, uid, ids, name, arg, context=None):
        res = {}
        for invoice in self.read(
                cr, uid, ids, ['picking_ids'], context=context):
            label = ''
            if invoice['picking_ids']:
                pickings = self.pool['stock.picking'].read(
                    cr, uid, invoice['picking_ids'], ['name'],
                    context=context)
                pick_names = []
                for picking in pickings:
                    pick_names.append(picking['name'])
                label = ','.join(pick_names)
            res[invoice['id']] = label
        return res

    _columns = {
        'picking_ids_label': fields.function(
            _compute_picking_ids_label, type='char', string='Pickings'),
        }
