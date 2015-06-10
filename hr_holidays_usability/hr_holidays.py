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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import logging

logger = logging.getLogger(__name__)


class HrHolidaysStatus(models.Model):
    _inherit = 'hr.holidays.status'

    vacation_compute_method = fields.Selection([
        ('worked', u'Jours ouvrés'),
        ('business', u'Jours ouvrables'),
        # TODO find proper English translation
        ], string='Vacation Compute Method', required=True,
        default='worked')


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'
    _order = 'type desc, date_from desc'
    # by default : type desc, date_from asc

# Idea :
# For allocation (type = add), we don't change anything:
# The user writes in the field number_of_days_temp and
# number_of_days = number_of_days_temp
# For leave (type = remove), we don't let users enter the number of days,
# we compute it for them
# -> new computed field "number_of_days_remove' that compute the number
# of days depending on the computation method defined on 'type'
# Redefine the field 'number_of_days' to take into accout
# 'number_of_days_remove' when type == remove (= number_of_days_remove * -1)
# change date time fields by date + selection morning/noon

# How do we set the dates :
# from : premier jour d'absence (et non dernier jour de présence)
#        + time : morning/noon
# to : date de fin de congés (et non date de retour au travail)
#      + time : noon/evening

# which computation methods on the 'hr.holidays.status':
# 1) jours ouvrés (sans compter les jours fériés)
# 2) jours ouvrables (quid des jours fériés ???) :
#    il faut compter les samedis sauf les samedis fériés.
#    Cas particulier : quand la personne prend le vendredi aprèm,
#    il faut compter 1j (et non 0.5 ni 1.5)
# 3) malade : on compte tous les jours -> ptet pas nécessaire pour le moment
# 1 for 'unpaid leaves' + repos compensateur + congés conventionnels + maladie
# 1 or 2 for normal holidays

    @api.one
    @api.depends(
        'vacation_date_from', 'vacation_time_from', 'vacation_date_to',
        'vacation_time_to', 'number_of_days_temp', 'type', 'holiday_type',
        'holiday_status_id.vacation_compute_method')
    def _compute_number_of_days(self):
        # depend on the holiday_status_id
        hhpo = self.env['hr.holidays.public']
        days = 0.0
        if (
                self.type == 'remove' and
                self.holiday_type == 'employee' and
                self.vacation_date_from and
                self.vacation_time_from and
                self.vacation_date_to and
                self.vacation_time_to):
            if self.holiday_status_id.vacation_compute_method == 'business':
                business = True
            else:
                business = False
            date_dt = start_date_dt = fields.Date.from_string(
                self.vacation_date_from)
            end_date_dt = fields.Date.from_string(
                self.vacation_date_to)

            while True:
                # REGULAR COMPUTATION
                # if it's a bank holidays, don't count
                if hhpo.is_public_holiday(date_dt, self.employee_id.id):
                    logger.info(
                        "%s is a bank holiday, don't count", date_dt)
                # it it's a saturday/sunday
                elif date_dt.weekday() in (5, 6):
                    logger.info(
                        "%s is a saturday/sunday, don't count", date_dt)
                else:
                    days += 1.0
                # special case for friday when compute_method = business
                if (
                        business and
                        date_dt.weekday() == 4 and
                        not hhpo.is_public_holiday(
                        date_dt + relativedelta(days=1),
                        self.employee_id.id)):
                    days += 1.0
                # PARTICULAR CASE OF THE FIRST DAY
                if date_dt == start_date_dt:
                    if self.vacation_time_from == 'noon':
                        if (
                                business and
                                date_dt.weekday() == 4 and
                                not hhpo.is_public_holiday(
                                date_dt + relativedelta(days=1),
                                self.employee_id.id)):
                            days -= 1.0  # result = 2 - 1 = 1
                        else:
                            days -= 0.5
                # PARTICULAR CASE OF THE LAST DAY
                if date_dt == end_date_dt:
                    if self.vacation_time_to == 'noon':
                        if (
                                business and
                                date_dt.weekday() == 4 and
                                not hhpo.is_public_holiday(
                                date_dt + relativedelta(days=1),
                                self.employee_id.id)):
                            days -= 1.5  # 2 - 1.5 = 0.5
                        else:
                            days -= 0.5
                    break
                date_dt += relativedelta(days=1)

        self.number_of_days_remove = days

        # PASTE
        if self.type == 'remove':
            # read number_of_days_remove instead of number_of_days_temp
            number_of_days = -days
        else:
            # for allocations, we read the native field number_of_days_temp
            number_of_days = self.number_of_days_temp
        self.number_of_days = number_of_days

    vacation_date_from = fields.Date(
        string='First Day of Vacation', track_visibility='onchange',
        help="Enter the first day of vacation. For example, if "
        "you leave one full calendar week, the first day of vacation "
        "is Monday morning (and not Friday of the week before)")
    vacation_time_from = fields.Selection([
        ('morning', 'Morning'),
        ('noon', 'Noon'),
        ], string="Start of Vacation", track_visibility='onchange',
        default='morning',
        help="For example, if you leave one full calendar week, "
        "the first day of vacation is Monday Morning")
    vacation_date_to = fields.Date(
        string='Last Day of Vacation', track_visibility='onchange',
        help="Enter the last day of vacation. For example, if you "
        "leave one full calendar week, the last day of vacation is "
        "Friday evening (and not Monday of the week after)")
    vacation_time_to = fields.Selection([
        ('noon', 'Noon'),
        ('evening', 'Evening'),
        ], string="End of Vacation", track_visibility='onchange',
        default='evening',
        help="For example, if you leave one full calendar week, "
        "the end of vacation is Friday Evening")
    number_of_days_remove = fields.Float(
        compute='_compute_number_of_days',
        string="Number of Days of Vacation", readonly=True)
    # number_of_days is a native field that I inherit
    number_of_days = fields.Float(compute='_compute_number_of_days')

    @api.one
    @api.constrains(
        'vacation_date_from', 'vacation_date_to', 'holiday_type', 'type')
    def _check_vacation_dates(self):
        hhpo = self.env['hr.holidays.public']
        if self.type == 'remove':
            if self.vacation_date_from > self.vacation_date_to:
                raise ValidationError(
                    _('The first day cannot be after the last day !'))
            elif (
                    self.vacation_date_from == self.vacation_date_to and
                    self.vacation_time_from == self.vacation_time_to):
                raise ValidationError(
                    _("The start of vacation is exactly the "
                        "same as the end !"))
            date_from_dt = fields.Date.from_string(
                self.vacation_date_from)
            if date_from_dt.weekday() in (5, 6):
                raise ValidationError(
                    _("The first day of vacation cannot be a "
                        "saturday or sunday !"))
            date_to_dt = fields.Date.from_string(
                self.vacation_date_to)
            if date_to_dt.weekday() in (5, 6):
                raise ValidationError(
                    _("The last day of Vacation cannot be a "
                        "saturday or sunday !"))
            if hhpo.is_public_holiday(date_from_dt, self.employee_id.id):
                raise ValidationError(
                    _("The first day of vacation cannot be a "
                        "bank holiday !"))
            if hhpo.is_public_holiday(date_to_dt, self.employee_id.id):
                raise ValidationError(
                    _("The last day of vacation cannot be a "
                        "bank holiday !"))

    @api.onchange('vacation_date_from', 'vacation_time_from')
    def vacation_from(self):
        hour = 0  # = morning
        if self.vacation_time_from and self.vacation_time_from == 'noon':
            hour = 12  # noon, LOCAL TIME
        datetime_str = False
        if self.vacation_date_from:
            date_dt = fields.Date.from_string(self.vacation_date_from)
            if self._context.get('tz'):
                localtz = pytz.timezone(self._context['tz'])
            else:
                localtz = pytz.utc
            datetime_dt = localtz.localize(datetime(
                date_dt.year, date_dt.month, date_dt.day, hour, 0, 0))
            # we give to odoo a datetime in UTC
            datetime_str = fields.Datetime.to_string(
                datetime_dt.astimezone(pytz.utc))
        self.date_from = datetime_str

    @api.onchange('vacation_date_to', 'vacation_time_to')
    def vacation_to(self):
        hour = 23  # = evening
        if self.vacation_time_to and self.vacation_time_to == 'noon':
            hour = 14  # Noon, LOCAL TIME
        datetime_str = False
        if self.vacation_date_to:
            date_dt = fields.Date.from_string(self.vacation_date_to)
            if self._context.get('tz'):
                localtz = pytz.timezone(self._context['tz'])
            else:
                localtz = pytz.utc
            datetime_dt = localtz.localize(datetime(
                date_dt.year, date_dt.month, date_dt.day, hour, 0, 0))
            # we give to odoo a datetime in UTC
            datetime_str = fields.Datetime.to_string(
                datetime_dt.astimezone(pytz.utc))
        self.date_to = datetime_str
