# coding: utf-8
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import collections
from openerp import models, fields, api


class ResourceCalendarAttendance(models.Model):
    _inherit = 'resource.calendar.attendance'

    # PR is done for v9
    # https://github.com/odoo/odoo/pull/10310
    calendar_id = fields.Many2one(ondelete='cascade')


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'
    _rec_name = 'display_name'

    hour_range = fields.Char(
        string='Hour Range', compute='_compute_hour_range',
        readonly=True, store=True,
        help="String representation of working hours")
    display_name = fields.Char(compute='_compute_display_name', store=True)

    @api.multi
    @api.depends('name', 'hour_range')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = "%s: %s" % (rec.name, rec.hour_range)

    @api.model
    def default_get(self, fields_list):
        "'attendance_ids' field default value"
        values = super(ResourceCalendar, self).default_get(fields_list)
        vals = []
        params = self.get_my_calendar_data()
        for hours in range(0, params.endday):
            mapping = self._populate_attendance(
                hours, params.hour_from, params.hour_to)
            vals.append((0, 0, mapping))
            if params.hour_from2 and params.hour_to2:
                mapping = self._populate_attendance(
                    hours, params.hour_from2, params.hour_to2)
                vals.append((0, 0, mapping))
        values['attendance_ids'] = vals
        return values

    @api.model
    def _populate_attendance(self, hours, hour_from, hour_to):
        return {
            'hour_from': hour_from,
            'hour_to': hour_to,
            'name': '.',
            'dayofweek': str(hours),
        }

    @api.model
    def get_my_calendar_data(self):
        'Override me according to your opening hours'
        Params = collections.namedtuple(
            'Params', 'hour_from hour_to hour_from2 hour_to2 endday')
        return Params(
            endday=5,
            hour_from=8,
            hour_to=12,
            # put hour_to/from to False if you don't want use them
            hour_from2=13,
            hour_to2=17,
        )

    @api.multi
    @api.depends('attendance_ids')
    def _compute_hour_range(self):
        for rec in self:
            if rec.attendance_ids:
                info = []
                dayofweek = ''
                for hours in rec.attendance_ids:
                    if hours.dayofweek != dayofweek:
                        selection = hours._fields['dayofweek'].selection
                        str_day = self.map_day()[
                            selection[int(hours.dayofweek)][1]]
                        info.append(
                            self.string_format(main_string=True) % (
                                str_day, int(hours.hour_from),
                                int(hours.hour_to)))
                    else:
                        # We are on the same day but with another hour range
                        # we concatenate on the first string of the day
                        position = info.index(info[-1:][0])
                        info[position] = self.string_format() % (
                            info[-1:][0], int(hours.hour_from),
                            int(hours.hour_to))
                    dayofweek = hours.dayofweek
                rec.hour_range = ', '.join(info)

    @api.model
    def string_format(self, main_string=None):
        'Override me to customize calendar hour_range'
        if main_string:
            # ie: 'Lu 8-12'
            return '%s %s-%s'
        # ie: 'Lu 8-12 / 13-17'
        return '%s / %s-%s'

    @api.model
    def map_day(self):
        'Override me to customize calendar hour_range'
        return {'Monday': 'Lu', 'Tuesday': 'Ma', 'Wednesday': 'Me',
                'Thursday': 'Je', 'Friday': 'Ve', 'Saturday': 'Sa',
                'Sunday': 'Di'}
