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

from openerp import fields, models, tools


class HrHolidaysEmployeeCounter(models.Model):
    _name = 'hr.holidays.employee.counter'
    _description = 'Counters for holidays of employees'
    _auto = False
    _rec_name = 'employee_id'
    _order = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    holiday_status_id = fields.Many2one(
        "hr.holidays.status", string="Leave Type")
    leaves_validated_current = fields.Float(string='Current Leaves Validated')
    leaves_validated_posted = fields.Float(string='Leaves Posted')
    leaves_remaining_current = fields.Float(string='Current Remaining Leaves')
    leaves_remaining_posted = fields.Float(string='Posted Remaining Leaves')
    allocated_leaves = fields.Float(string='Allocated Leaves')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'hr_holidays_employee_counter')
        cr.execute("""
            CREATE or REPLACE view hr_holidays_employee_counter AS (
                SELECT
                    min(hh.id) AS id,
                    hh.employee_id AS employee_id,
                    hh.holiday_status_id AS holiday_status_id,
                    sum(
                        CASE WHEN hh.type='remove'
                        THEN hh.number_of_days * -1
                        ELSE 0
                        END) AS leaves_validated_current,
                    sum(
                        CASE WHEN hh.type='remove'
                            AND hh.posted_date IS NOT null
                        THEN hh.number_of_days * -1
                        ELSE 0
                        END) AS leaves_validated_posted,
                    sum(hh.number_of_days) AS leaves_remaining_current,
                    sum(
                        CASE WHEN (
                            hh.type='remove' AND hh.posted_date IS NOT null)
                            OR hh.type='add'
                        THEN hh.number_of_days
                        ELSE 0
                        END) as leaves_remaining_posted,
                    sum(
                        CASE WHEN hh.type = 'add'
                        THEN hh.number_of_days
                        ELSE 0
                        END) AS allocated_leaves
                FROM
                    hr_holidays hh
                    JOIN hr_holidays_status hhs
                        ON (hhs.id=hh.holiday_status_id)
                WHERE
                    hh.state='validate' AND
                    hhs.limit=False
                GROUP BY hh.employee_id, hh.holiday_status_id
            )
            """)
