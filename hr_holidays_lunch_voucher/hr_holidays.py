# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    lunch_voucher_id = fields.Many2one(
        'lunch.voucher.attribution',
        string="Related Lunch Voucher Attribution")
    lunch_voucher_remove_qty = fields.Integer(
        compute='_compute_lunch_voucher_remove_qty', readonly=True,
        store=True, string='Lunch Vouchers to Deduct')

    @api.depends('employee_id', 'vacation_date_from', 'vacation_date_to')
    def _compute_lunch_voucher_remove_qty(self):
        hhpo = self.env['hr.holidays.public']
        for hol in self:
            qty = 0
            if (
                    hol.type == 'remove' and
                    hol.vacation_date_from and
                    hol.vacation_date_to):
                start_date_dt = fields.Date.from_string(hol.vacation_date_from)
                end_date_str = hol.vacation_date_to
                date_dt = start_date_dt
                # Remove 1 full LV when vacation_time_from == noon
                # and also when vacation_time_to == noon
                while True:
                    if (
                            date_dt.weekday() not in (5, 6) and
                            not hhpo.is_public_holiday(
                                date_dt, hol.employee_id.id)):
                        qty += 1
                    date_dt += relativedelta(days=1)
                    date_str = fields.Date.to_string(date_dt)
                    if date_str > end_date_str:
                        break
            hol.lunch_voucher_remove_qty = qty
