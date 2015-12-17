# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Date Planned Update module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
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
from openerp.tools.translate import _


class PoDatePlannedUpdate(orm.TransientModel):
    _name = 'po.date.planned.update'
    _description = 'Update Scheduled Date on PO'

    _columns = {
        'date_planned': fields.date('New Scheduled Date', required=True),
        }

    def run(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        assert len(ids) == 1, '1 ID'
        wiz = self.browse(cr, uid, ids[0], context=context)
        assert context.get('active_model') == 'purchase.order',\
            'wrong active model'
        assert context.get('active_id'), 'Missing active_id in ctx'
        today = fields.date.context_today(self, cr, uid, context=context)
        if wiz.date_planned < today:
            raise orm.except_orm(
                _('Error'),
                _("The new scheduled date should not be in the past !"))
        polo = self.pool['purchase.order.line']
        pol_ids = polo.search(cr, uid, [
            ('order_id', '=', context['active_id'])], context=context)
        if pol_ids:
            polo.write(cr, uid, pol_ids, {
                'date_planned': wiz.date_planned}, context=context)
        else:
            raise orm.except_orm(
                _('Error'),
                _("This PO doesn't have purchase order line"))
        return True
