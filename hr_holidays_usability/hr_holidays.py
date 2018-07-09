# -*- coding: utf-8 -*-
# © 2015-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
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
    add_validation_manager = fields.Boolean(
        string='Allocation validated by HR Manager',
        help="If enabled, allocation requests for this leave type "
        "can be validated only by an HR Manager "
        "(not possible by an HR Officer).")


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    holiday_exclude_mass_allocation = fields.Boolean(
        string='Exclude from Mass Holiday Allocation')


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

# Idea :
# For allocation (type = add), we don't change anything:
# The user writes in the field number_of_days_temp and
# number_of_days = number_of_days_temp
# IN 7.0: For leave (type = remove), we don't let users enter the number
# of days, we compute it for them
# -> new computed field "number_of_days_remove' that compute the number
# of days depending on the computation method defined on 'type'
# Redefine the field 'number_of_days' to take into accout
# 'number_of_days_remove' when type == remove (= number_of_days_remove * -1)
# IN 8.0: for leaves, use the on_change on the dates to set the
# number_of_days_temp. But we want to have this field readonly, so we also
# inherit write + create (even in v8, readonly fields are not written in DB)

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

    @api.model
    def _usability_compute_number_of_days(self):
        # depend on the holiday_status_id
        hhpo = self.env['hr.holidays.public']
        days = 0.0
        if (
                self.type == 'remove' and
                self.holiday_type == 'employee' and
                self.vacation_date_from and
                self.vacation_time_from and
                self.vacation_date_to and
                self.vacation_time_to and
                self.vacation_date_from <= self.vacation_date_to):
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
        return days

    @api.depends('holiday_type', 'employee_id', 'holiday_status_id')
    def _compute_current_leaves(self):
        for holi in self:
            total_allocated_leaves = 0
            current_leaves_taken = 0
            current_remaining_leaves = 0
            if (
                    holi.holiday_type == 'employee' and
                    holi.employee_id and
                    holi.holiday_status_id):
                days = holi.holiday_status_id.get_days(holi.employee_id.id)
                total_allocated_leaves =\
                    days[holi.holiday_status_id.id]['max_leaves']
                current_leaves_taken =\
                    days[holi.holiday_status_id.id]['leaves_taken']
                current_remaining_leaves =\
                    days[holi.holiday_status_id.id]['remaining_leaves']
            holi.total_allocated_leaves = total_allocated_leaves
            holi.current_leaves_taken = current_leaves_taken
            holi.current_remaining_leaves = current_remaining_leaves

    @api.depends('payslip_date')
    def _compute_payslip_status(self):
        for holi in self:
            if holi.payslip_date:
                holi.payslip_status = True
            else:
                holi.payslip_status = False

    def _set_payslip_status(self):
        for holi in self:
            if holi.payslip_status:
                holi.payslip_date = fields.Date.context_today(self)
            else:
                holi.payslip_date = False

    vacation_date_from = fields.Date(
        string='First Day of Vacation', track_visibility='onchange',
        readonly=True, states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)]},
        help="Enter the first day of vacation. For example, if "
        "you leave one full calendar week, the first day of vacation "
        "is Monday morning (and not Friday of the week before)")
    vacation_time_from = fields.Selection([
        ('morning', 'Morning'),
        ('noon', 'Noon'),
        ], string="Start of Vacation", track_visibility='onchange',
        default='morning', readonly=True, states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)]},
        help="For example, if you leave one full calendar week, "
        "the first day of vacation is Monday Morning")
    vacation_date_to = fields.Date(
        string='Last Day of Vacation', track_visibility='onchange',
        readonly=True, states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)]},
        help="Enter the last day of vacation. For example, if you "
        "leave one full calendar week, the last day of vacation is "
        "Friday evening (and not Monday of the week after)")
    vacation_time_to = fields.Selection([
        ('noon', 'Noon'),
        ('evening', 'Evening'),
        ], string="End of Vacation", track_visibility='onchange',
        default='evening', readonly=True, states={
            'draft': [('readonly', False)],
            'confirm': [('readonly', False)]},
        help="For example, if you leave one full calendar week, "
        "the end of vacation is Friday Evening")
    current_leaves_taken = fields.Float(
        compute='_compute_current_leaves', string='Current Leaves Taken',
        readonly=True)
    current_remaining_leaves = fields.Float(
        compute='_compute_current_leaves', string='Current Remaining Leaves',
        readonly=True)
    total_allocated_leaves = fields.Float(
        compute='_compute_current_leaves', string='Total Allocated Leaves',
        readonly=True)
    limit = fields.Boolean(  # pose des pbs de droits
        related='holiday_status_id.limit', string='Allow to Override Limit',
        readonly=True, compute_sudo=True)
    payslip_date = fields.Date(
        string='Transfer to Payslip Date', track_visibility='onchange',
        readonly=True)
    # even with the new boolean field "payslip_status", I want to keep
    # the "posted_date" (renamed payslip_date) field, because I want structured
    # info. The main argument is that, if I don't write down the info at the end
    # of the wizard "Post Leave Requests", I want to easily
    # re-display the info
    payslip_status = fields.Boolean(
        readonly=True, compute='_compute_payslip_status',
        inverse='_set_payslip_status', store=True, track_visibility='onchange')
    number_of_days_temp = fields.Float(string="Number of days")
    # The 'name' field is displayed publicly in the calendar
    # So the label should not be 'Description' but 'Public Title'
    name = fields.Char(
        string='Public Title',
        help="Warning: this title is shown publicly in the "
        "calendar. Don't write private/personnal information in this field.")
    # by default, there is no company_id field on hr.holidays !
    company_id = fields.Many2one(
        related='employee_id.resource_id.company_id', store=True,
        readonly=True, compute_sudo=True)
    state = fields.Selection(default='draft')  # hr_holidays, default='confirm'

    @api.constrains(
        'vacation_date_from', 'vacation_date_to', 'holiday_type', 'type')
    def _check_vacation_dates(self):
        hhpo = self.env['hr.holidays.public']
        for holi in self:
            if holi.type == 'remove':
                if holi.vacation_date_from > holi.vacation_date_to:
                    raise ValidationError(_(
                        'The first day cannot be after the last day !'))
                elif (
                        holi.vacation_date_from == holi.vacation_date_to and
                        holi.vacation_time_from == holi.vacation_time_to):
                    raise ValidationError(_(
                        "The start of vacation is exactly the "
                        "same as the end !"))
                date_from_dt = fields.Date.from_string(
                    holi.vacation_date_from)
                if date_from_dt.weekday() in (5, 6):
                    raise ValidationError(_(
                        "The first day of vacation cannot be a "
                        "saturday or sunday !"))
                date_to_dt = fields.Date.from_string(
                    holi.vacation_date_to)
                if date_to_dt.weekday() in (5, 6):
                    raise ValidationError(_(
                        "The last day of Vacation cannot be a "
                        "saturday or sunday !"))
                if hhpo.is_public_holiday(date_from_dt, holi.employee_id.id):
                    raise ValidationError(_(
                        "The first day of vacation cannot be a "
                        "bank holiday !"))
                if hhpo.is_public_holiday(date_to_dt, holi.employee_id.id):
                    raise ValidationError(_(
                        "The last day of vacation cannot be a "
                        "bank holiday !"))

    @api.onchange('vacation_date_from', 'vacation_time_from')
    def vacation_from(self):
        hour = 5  # = morning
        if self.vacation_time_from and self.vacation_time_from == 'noon':
            hour = 13  # noon, LOCAL TIME
            # Warning : when the vacation STARTs at Noon, it starts at 1 p.m.
            # to avoid an overlap (which would be blocked by a constraint of
            # hr_holidays) if a user requests 2 half-days with different
            # holiday types on the same day
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
        hour = 22  # = evening
        if self.vacation_time_to and self.vacation_time_to == 'noon':
            hour = 12  # Noon, LOCAL TIME
            # Warning : when vacation STOPs at Noon, it stops at 12 a.m.
            # to avoid an overlap (which would be blocked by a constraint of
            # hr_holidays) if a user requests 2 half-days with different
            # holiday types on the same day
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

    @api.onchange(
        'vacation_date_from', 'vacation_time_from', 'vacation_date_to',
        'vacation_time_to', 'number_of_days_temp', 'type', 'holiday_type',
        'holiday_status_id')
    def leave_number_of_days_change(self):
        if self.type == 'remove':
            days = self._usability_compute_number_of_days()
            self.number_of_days_temp = days

    # Neutralize the native on_change on dates
    def _onchange_date_from(self):
        return {}

    def _onchange_date_to(self):
        return {}

    # I want to set number_of_days_temp as readonly in the view of leaves
    # and, even in v8, we can't write on a readonly field
    # So I inherit write and create
    @api.model
    def create(self, vals):
        obj = super(HrHolidays, self).create(vals)
        if obj.type == 'remove':
            days = obj._usability_compute_number_of_days()
            obj.number_of_days_temp = days
        return obj

    @api.multi
    def write(self, vals):
        res = super(HrHolidays, self).write(vals)
        for obj in self:
            if obj.type == 'remove':
                days = obj._usability_compute_number_of_days()
                if days != obj.number_of_days_temp:
                    obj.number_of_days_temp = days
        return res

    @api.multi
    def action_confirm(self):
        for holi in self:
            if not self._context.get('no_email_notification'):
                template = self.env.ref(
                    'hr_holidays_usability.email_template_hr_holidays')
                template.with_context(
                    dbname=self._cr.dbname,
                    new_holiday_state='submitted').send_mail(holi.id)
        return super(HrHolidays, self).action_confirm()

    @api.multi
    def action_validate(self):
        for holi in self:
            if holi.user_id == self.env.user:
                if holi.type == 'remove':
                    raise UserError(_(
                        "You cannot validate your own Leave request '%s'.")
                        % holi.name)
                elif (
                        holi.type == 'add' and
                        not self.env.user.has_group(
                            'hr_holidays.group_hr_holidays_manager')):
                    raise UserError(_(
                        "You cannot validate your own Allocation "
                        "request '%s'.") % holi.name)
            if (
                    holi.type == 'add' and
                    holi.holiday_status_id.add_validation_manager and
                    not self.env.user.has_group(
                        'hr_holidays.group_hr_holidays_manager')):
                raise UserError(_(
                    "Allocation request '%s' has a leave type '%s' that "
                    "can be approved only by an HR Manager.")
                    % (holi.name, holi.holiday_status_id.name))
            if not self._context.get('no_email_notification'):
                template = self.env.ref(
                    'hr_holidays_usability.email_template_hr_holidays')
                template.with_context(
                    dbname=self._cr.dbname,
                    new_holiday_state='validated').send_mail(holi.id)
        return super(HrHolidays, self).action_validate()

    @api.multi
    def action_refuse(self):
        for holi in self:
            if (
                    holi.user_id == self.env.user and
                    not self.env.user.has_group(
                        'hr_holidays.group_hr_holidays_manager')):
                raise UserError(_(
                    "You cannot refuse your own Leave or Allocation "
                    "holiday request '%s'.")
                    % holi.name)
            if not self._context.get('no_email_notification'):
                template = self.env.ref(
                    'hr_holidays_usability.email_template_hr_holidays')
                template.with_context(
                    dbname=self._cr.dbname,
                    new_holiday_state='refused').send_mail(holi.id)
        return super(HrHolidays, self).action_refuse()


class ResCompany(models.Model):
    _inherit = 'res.company'

    mass_allocation_default_holiday_status_id = fields.Many2one(
        'hr.holidays.status', string='Default Leave Type for Mass Allocation')


class BaseConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    mass_allocation_default_holiday_status_id = fields.Many2one(
        related='company_id.mass_allocation_default_holiday_status_id', compute_sudo=True)
