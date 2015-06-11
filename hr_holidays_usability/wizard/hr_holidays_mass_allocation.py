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
from openerp import netsvc


class HrHolidaysMassAllocation(orm.TransientModel):
    _name = 'hr.holidays.mass.allocation'
    _description = 'Wizard for mass allocation of holidays'

    def _get_all_employees(self, cr, uid, context=None):
        return self.pool['hr.employee'].search(cr, uid, [], context=context)

    def _get_default_holiday_status(self, cr, uid, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        if user.company_id.mass_allocation_default_holiday_status_id:
            return user.company_id.mass_allocation_default_holiday_status_id.id
        else:
            return False

    _columns = {
        'number_of_days': fields.float('Number of Days', required=True),
        'holiday_status_id': fields.many2one(
            'hr.holidays.status', 'Leave Type', required=True),
        'employee_ids': fields.many2many(
            'hr.employee', string='Employees'),
        'auto_approve': fields.boolean('Automatic Approval'),
        # size=64 because the name field of hr.holidays is size=64
        'name': fields.char('Description', size=64),
        }

    _defaults = {
        'number_of_days': 2.08,
        'employee_ids': _get_all_employees,
        'auto_approve': True,
        'holiday_status_id': _get_default_holiday_status,
    }

    _sql_constraints = [(
        'number_of_days_positive',
        'CHECK (number_of_days > 0)',
        'The number of days must be positive',
        )]

    def run(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'Only 1 ID'
        wiz = self.browse(cr, uid, ids[0], context=context)
        if not wiz.number_of_days:
            raise orm.except_orm(
                _('Error:'),
                _('You must set a value for the number of days.'))
        if not wiz.employee_ids:
            raise orm.except_orm(
                _('Error:'),
                _('You must select at least one employee.'))
        alloc_hol_ids = []
        hho = self.pool['hr.holidays']
        wf_service = netsvc.LocalService("workflow")
        auto_approve = wiz.auto_approve
        for employee in wiz.employee_ids:
            hol_id = hho.create(cr, uid, {
                'name': wiz.name,
                'number_of_days_temp': wiz.number_of_days,
                'employee_id': employee.id,
                'type': 'add',
                'holiday_type': 'employee',
                'holiday_status_id': wiz.holiday_status_id.id,
                }, context=context)
            if auto_approve:
                wf_service.trg_validate(
                    uid, 'hr.holidays', hol_id, 'validate', cr)
            alloc_hol_ids.append(hol_id)
        act_model, act_id = self.pool['ir.model.data'].get_object_reference(
            cr, uid, 'hr_holidays', 'open_allocation_holidays')
        assert act_model == 'ir.actions.act_window', 'Wrong model'
        action = self.pool[act_model].read(
            cr, uid, act_id, context=context)
        action.update({
            'target': 'current',
            'domain': [('id', 'in', alloc_hol_ids)],
            'nodestroy': True,
            'context': context,
            })
        return action
