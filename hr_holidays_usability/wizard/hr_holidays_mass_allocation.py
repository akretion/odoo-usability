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

from openerp import models, fields, api, workflow, _
from openerp.exceptions import Warning


class HrHolidaysMassAllocation(models.TransientModel):
    _name = 'hr.holidays.mass.allocation'
    _description = 'Wizard for mass allocation of holidays'

    @api.model
    def _default_employees(self):
        return self.env['hr.employee'].search([
            ('holiday_exclude_mass_allocation', '=', False),
            ('company_id', '=', self.env.user.company_id.id),
            ])

    @api.model
    def _get_default_holiday_status(self):
        res = self.env.user.company_id.\
            mass_allocation_default_holiday_status_id or False
        return res

    number_of_days = fields.Float(
        string='Number of Days', required=True, default=2.08)
    holiday_status_id = fields.Many2one(
        'hr.holidays.status', string='Leave Type', required=True,
        default=_get_default_holiday_status)
    employee_ids = fields.Many2many(
        'hr.employee', string='Employees', default=_default_employees)
    auto_approve = fields.Boolean(
        string='Automatic Approval', default=True)
    # size=64 because the name field of hr.holidays is size=64
    name = fields.Char('Description', size=64)

    _sql_constraints = [(
        'number_of_days_positive',
        'CHECK (number_of_days > 0)',
        'The number of days must be positive',
        )]

    @api.multi
    def run(self):
        self.ensure_one()
        if not self.number_of_days:
            raise Warning(
                _('You must set a value for the number of days.'))
        if not self.employee_ids:
            raise Warning(
                _('You must select at least one employee.'))
        alloc_hol_ids = []
        hho = self.env['hr.holidays']
        auto_approve = self.auto_approve
        for employee in self.employee_ids:
            hol = hho.create({
                'name': self.name,
                'number_of_days_temp': self.number_of_days,
                'employee_id': employee.id,
                'type': 'add',
                'holiday_type': 'employee',
                'holiday_status_id': self.holiday_status_id.id,
                'no_email_notification': True,
                })
            if auto_approve:
                workflow.trg_validate(
                    self._uid, 'hr.holidays', hol.id, 'validate', self._cr)
            alloc_hol_ids.append(hol.id)
        action = self.env['ir.actions.act_window'].for_xml_id(
            'hr_holidays', 'open_allocation_holidays')
        action.update({
            'target': 'current',
            'domain': [('id', 'in', alloc_hol_ids)],
            'nodestroy': True,
            'context': "{'default_type':'add'}",
            })
        return action
