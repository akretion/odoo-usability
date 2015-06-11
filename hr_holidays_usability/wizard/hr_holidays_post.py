# -*- encoding: utf-8 -*-
##############################################################################
#
#    HR Holidays Usability module for Odoo
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


class HrHolidaysPost(orm.TransientModel):
    _name = 'hr.holidays.post'
    _description = 'Wizard for post holidays'

    _columns = {
        'before_date': fields.date(
            'Select Holidays That Ended Before', required=True,
            help="The wizard will select the validated holidays "
            "that ended before that date (including holidays that "
            "ended on that date)."),
        'holidays_to_post_ids': fields.many2many(
            'hr.holidays', string='Leave Requests to Post',
            domain=[
                ('type', '=', 'remove'),
                ('holiday_type', '=', 'employee'),
                ('state', '=', 'validate'),
                ('posted_date', '=', False),
                ]),
        'state': fields.selection([
            ('draft', 'Draft'),
            ('done', 'Done'),
            ], 'State', readonly=True),
        }

    _defaults = {
        'before_date': fields.date.context_today,
        'state': 'draft',
    }

    def select_date(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only 1 ID'
        wiz = self.browse(cr, uid, ids[0], context=context)
        hol_ids = self.pool['hr.holidays'].search(cr, uid, [
            ('type', '=', 'remove'),
            ('holiday_type', '=', 'employee'),
            ('state', '=', 'validate'),
            ('posted_date', '=', False),
            ('vacation_date_to', '<=', wiz.before_date),
            ], context=context)
        self.write(cr, uid, ids, {
            'state': 'done',
            'holidays_to_post_ids': [(6, 0, hol_ids)],
            }, context=context)
        act_model, act_id = self.pool['ir.model.data'].get_object_reference(
            cr, uid, 'hr_holidays_usability', 'hr_holidays_post_action')
        assert act_model == 'ir.actions.act_window', 'Wrong model'
        action = self.pool[act_model].read(
            cr, uid, act_id, context=context)
        action['res_id'] = ids[0]
        return action

    def run(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only 1 ID'
        wiz = self.browse(cr, uid, ids[0], context=context)
        today = fields.date.context_today(self, cr, uid, context=context)
        if not wiz.holidays_to_post_ids:
            raise orm.except_orm(
                _('Error:'),
                _('No  for the number of days.'))
        hol_ids = self.read(
            cr, uid, ids[0], context=context)['holidays_to_post_ids']
        self.pool['hr.holidays'].write(
            cr, uid, hol_ids,
            {'posted_date': today}, context=context)
        # On v8, return a graph view !
        act_model, act_id = self.pool['ir.model.data'].get_object_reference(
            cr, uid, 'hr_holidays', 'open_ask_holidays')
        assert act_model == 'ir.actions.act_window', 'Wrong model'
        action = self.pool[act_model].read(
            cr, uid, act_id, context=context)
        action.update({
            'target': 'current',
            'domain': [('id', 'in', hol_ids)],
            'nodestroy': True,
            'context': {'group_by': ['employee_id', 'holiday_status_id']},
            })
        return action
