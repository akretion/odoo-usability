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
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, \
    DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz
import logging

logger = logging.getLogger(__name__)


class HrHolidaysStatus(orm.Model):
    _inherit = 'hr.holidays.status'

    _columns = {
        'vacation_compute_method': fields.selection([
            ('worked', u'Jours ouvrés'),
            ('business', u'Jours ouvrables'),
            # TODO find proper English translation
            ], 'Vacation Compute Method', required=True),
        }

    _defaults = {
        'vacation_compute_method': 'worked',
        }


class HrHolidays(orm.Model):
    _inherit = 'hr.holidays'
    _order = 'type desc, date_from desc'
    # by default : type desc, date_from asc

# Idea :
# For allocation (type = add), we don't change anything
# For leave (type = remove), we don't let users enter the number of days, we compute it for them
# -> new computed field "number_of_days_remove' that compute the number of days depending on the computation method defined on 'type'
# Redefine the field 'number_of_days' to take into accout 'number_of_days_remove' when type == remove
# change date time fields by date + selection morning/noon

# How do we set the dates :
# from : premier jour d'absence (et non dernier jour de présence) + time : morning/noon
# to : date de fin de congés (et non date de retour au travail) + time : noon/evening

# which computation methods on the 'hr.holidays.status':
# 1) jours ouvrés (sans compter les jours fériés)
# 2) jours ouvrables (quid des jours fériés ???) : il faut compter les samedis sauf les samedis fériés. Cas particulier : quand la personne prend le vendredi aprèm, il faut compter 1j (et non 0.5 ni 1.5)
# 3) malade : on compte tous les jours -> ptet pas nécessaire pour le moment
# 1 for 'unpaid leaves' + repos compensateur + congés conventionnels + maladie
# 1 or 2 for normal holidays

    def _compute_number_of_days(self, cr, uid, ids, name, args, context=None):
        result = {}
        for hol in self.browse(cr, uid, ids, context=context):
            if hol.type == 'remove':
                # read number_of_days_remove instead of number_of_days_temp
                result[hol.id] = -hol.number_of_days_remove
            else:
                # for allocations, we read the native field number_of_days_temp
                result[hol.id] = hol.number_of_days_temp
        return result

    def _compute_number_of_days_remove(
            self, cr, uid, ids, name, args, context=None):
        res = {}
        # depend on the holiday_status_id
        hhpo = self.pool['hr.holidays.public']
        for hol in self.browse(cr, uid, ids, context=context):
            days = 0.0
            if hol.type == 'remove' and hol.holiday_type == 'employee':
                if hol.holiday_status_id.vacation_compute_method == 'business':
                    business = True
                else:
                    business = False
                date_dt = start_date_dt = datetime.strptime(
                    hol.vacation_date_from, DEFAULT_SERVER_DATE_FORMAT)
                end_date_dt = datetime.strptime(
                    hol.vacation_date_to, DEFAULT_SERVER_DATE_FORMAT)

                while True:
                    # REGULAR COMPUTATION
                    # if it's a bank holidays, don't count
                    if hhpo.is_public_holiday(
                            cr, uid, date_dt, hol.employee_id.id,
                            context=context):
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
                            business
                            and date_dt.weekday() == 4
                            and not hhpo.is_public_holiday(
                            cr, uid, date_dt + relativedelta(days=1),
                            hol.employee_id.id, context=context)):
                        days += 1.0
                    # PARTICULAR CASE OF THE FIRST DAY
                    if date_dt == start_date_dt:
                        if hol.vacation_time_from == 'noon':
                            if (
                                    business
                                    and date_dt.weekday() == 4
                                    and not hhpo.is_public_holiday(
                                    cr, uid, date_dt + relativedelta(days=1),
                                    hol.employee_id.id, context=context)):
                                days -= 1.0  # result = 2 - 1 = 1
                            else:
                                days -= 0.5
                    # PARTICULAR CASE OF THE LAST DAY
                    if date_dt == end_date_dt:
                        if hol.vacation_time_to == 'noon':
                            if (
                                    business
                                    and date_dt.weekday() == 4
                                    and not hhpo.is_public_holiday(
                                    cr, uid, date_dt + relativedelta(days=1),
                                    hol.employee_id.id, context=context)):
                                days -= 1.5  # 2 - 1.5 = 0.5
                            else:
                                days -= 0.5
                        break
                    date_dt += relativedelta(days=1)

            res[hol.id] = days
        return res

    _columns = {
        'vacation_date_from': fields.date(
            'First Day of Vacation', track_visibility='onchange',
            help="Enter the first day of vacation. For example, if "
            "you leave one full calendar week, the first day of vacation "
            "is Monday morning (and not Friday of the week before)"),
        'vacation_time_from': fields.selection([
            ('morning', 'Morning'),
            ('noon', 'Noon'),
            ], "Start of Vacation", track_visibility='onchange',
            help="For example, if you leave one full calendar week, "
            "the first day of vacation is Monday Morning"),
        'vacation_date_to': fields.date(
            'Last Day of Vacation', track_visibility='onchange',
            help="Enter the last day of vacation. For example, if you "
            "leave one full calendar week, the last day of vacation is "
            "Friday evening (and not Monday of the week after)"),
        'vacation_time_to': fields.selection([
            ('noon', 'Noon'),
            ('evening', 'Evening'),
            ], "End of Vacation", track_visibility='onchange',
            help="For example, if you leave one full calendar week, "
            "the end of vacation is Friday Evening"),
        'number_of_days_remove': fields.function(
            _compute_number_of_days_remove,
            string="Number of Days of Vacation",
            type="float", readonly=True),
        # number_of_days is a native field that I inherit
        'number_of_days': fields.function(
            _compute_number_of_days, string='Number of Days', store=True),
        }

    _defaults = {
        'vacation_time_from': 'morning',
        'vacation_time_to': 'evening',
        }

    def _check_vacation_dates(self, cr, uid, ids):
        hhpo = self.pool['hr.holidays.public']
        for hol in self.browse(cr, uid, ids):
            if hol.type == 'remove':
                if hol.vacation_date_from > hol.vacation_date_to:
                    raise orm.except_orm(
                        _('Error:'),
                        _('The first day cannot be after the last day !'))
                elif (
                        hol.vacation_date_from == hol.vacation_date_to
                        and hol.vacation_time_from == hol.vacation_time_to):
                    raise orm.except_orm(
                        _('Error:'),
                        _("The start of vacation is exactly the "
                            "same as the end !"))
                date_from_dt = datetime.strptime(
                    hol.vacation_date_from, DEFAULT_SERVER_DATE_FORMAT)
                if date_from_dt.weekday() in (5, 6):
                    raise orm.except_orm(
                        _('Error:'),
                        _("The first day of vacation cannot be a "
                            "saturday or sunday !"))
                date_to_dt = datetime.strptime(
                    hol.vacation_date_to, DEFAULT_SERVER_DATE_FORMAT)
                if date_to_dt.weekday() in (5, 6):
                    raise orm.except_orm(
                        _('Error:'),
                        _("The last day of Vacation cannot be a "
                            "saturday or sunday !"))
                if hhpo.is_public_holiday(
                        cr, uid, date_from_dt, hol.employee_id.id):
                    raise orm.except_orm(
                        _('Error:'),
                        _("The first day of vacation cannot be a "
                            "bank holiday !"))
                if hhpo.is_public_holiday(
                        cr, uid, date_to_dt, hol.employee_id.id):
                    raise orm.except_orm(
                        _('Error:'),
                        _("The last day of vacation cannot be a "
                            "bank holiday !"))
        return True

    _constraints = [(
        _check_vacation_dates,
        'error msg in raise',
        ['vacation_date_from', 'vacation_date_to', 'holiday_type', 'type'],
    )]

    def vacation_from(
            self, cr, uid, ids, vacation_date_from, vacation_time_from,
            context=None):
        if context is None:
            context = {}
        hour = 0  # = morning
        if vacation_time_from and vacation_time_from == 'noon':
            hour = 12  # noon, LOCAL TIME
        datetime_str = False
        if vacation_date_from:
            date_dt = datetime.strptime(
                vacation_date_from, DEFAULT_SERVER_DATE_FORMAT)
            if context.get('tz'):
                localtz = pytz.timezone(context['tz'])
            else:
                localtz = pytz.utc
            datetime_dt = localtz.localize(datetime(
                date_dt.year, date_dt.month, date_dt.day, hour, 0, 0))
            # we give to odoo a datetime in UTC
            datetime_str = datetime_dt.astimezone(pytz.utc).strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
        return {'value': {'date_from': datetime_str}}

    def vacation_to(
            self, cr, uid, ids, vacation_date_to, vacation_time_to,
            context=None):
        hour = 23  # = evening
        if vacation_time_to and vacation_time_to == 'noon':
            hour = 14  # Noon, LOCAL TIME
        datetime_str = False
        if vacation_date_to:
            date_dt = datetime.strptime(
                vacation_date_to, DEFAULT_SERVER_DATE_FORMAT)
            if context.get('tz'):
                localtz = pytz.timezone(context['tz'])
            else:
                localtz = pytz.utc
            datetime_dt = localtz.localize(datetime(
                date_dt.year, date_dt.month, date_dt.day, hour, 0, 0))
            # we give to odoo a datetime in UTC
            datetime_str = datetime_dt.astimezone(pytz.utc).strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
        return {'value': {'date_to': datetime_str}}
