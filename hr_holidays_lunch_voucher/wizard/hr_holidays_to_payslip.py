# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)


class HrHolidaysToPayslip(models.TransientModel):
    _inherit = 'hr.holidays.to.payslip'

    lunch_voucher_po = fields.Boolean(
        string='Generate Lunch Voucher Purchase Order')
    work_days = fields.Integer(string='Work Days')

    @api.model
    def default_get(self, fields_list):
        res = super(HrHolidaysToPayslip, self).default_get(fields_list)
        hhpo = self.env['hr.holidays.public']
        company = self.env.user.company_id
        if company.lunch_voucher_product_id:
            res['lunch_voucher_po'] = True
        today = fields.Date.context_today(self)
        today_dt = fields.Date.from_string(today)
        cur_month = today_dt.month
        # last day of month
        date_dt = today_dt + relativedelta(day=31)
        work_days = date_dt.day
        logger.info('Number of days in the month: %d', work_days)
        # from last day of month to the first
        while date_dt.month == cur_month:
            if hhpo.is_public_holiday(date_dt):
                work_days -= 1
                logger.info(
                    "%s is a bank holiday, don't count", date_dt)
            # if it's a saturday/sunday
            elif date_dt.weekday() in (5, 6):
                work_days -= 1
                logger.info(
                    "%s is a saturday/sunday, don't count", date_dt)
            date_dt += relativedelta(days=-1)
        logger.info('Number of work days in the month: %d', work_days)
        res['work_days'] = work_days
        return res

    def run(self):
        self.ensure_one()
        lvao = self.env['lunch.voucher.attribution']
        today = fields.Date.context_today(self)
        employees = self.env['hr.employee'].search([
            ('lunch_voucher', '=', True),
            ('company_id', '=', self.env.user.company_id.id),
            ])
        lv_dict = {}
        for employee in employees:
            lv_dict[employee.id] = []
        for hol in self.holidays_to_payslip_ids:
            if not hol.lunch_voucher_id and hol.employee_id.id in lv_dict:
                lv_dict[hol.employee_id.id].append(hol.id)
        for employee_id, hol_ids in lv_dict.iteritems():
            vals = {
                'employee_id': employee_id,
                'date': today,
                'month_work_days': self.work_days,
                }
            if hol_ids:
                vals['holiday_ids'] = [(6, 0, hol_ids)]
            lvao.create(vals)
        return super(HrHolidaysToPayslip, self).run()
