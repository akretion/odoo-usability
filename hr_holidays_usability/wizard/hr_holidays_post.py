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
from openerp.exceptions import Warning


class HrHolidaysPost(models.TransientModel):
    _name = 'hr.holidays.post'
    _description = 'Wizard for post holidays'

    before_date = fields.Date(
        string='Select Leave Requests That Ended Before', required=True,
        default=fields.Date.context_today,
        help="The wizard will select the validated holidays "
        "that ended before that date (including holidays that "
        "ended on that date).")
    holidays_to_post_ids = fields.Many2many(
        'hr.holidays', string='Leave Requests to Post',
        domain=[
            ('type', '=', 'remove'),
            ('holiday_type', '=', 'employee'),
            ('state', '=', 'validate'),
            ('posted_date', '=', False),
            ])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], string='State', readonly=True, default='draft')

    @api.multi
    def select_date(self):
        self.ensure_one()
        hols = self.env['hr.holidays'].search([
            ('type', '=', 'remove'),
            ('holiday_type', '=', 'employee'),
            ('state', '=', 'validate'),
            ('posted_date', '=', False),
            ('vacation_date_to', '<=', self.before_date),
            ('company_id', '=', self.env.user.company_id.id),
            ])
        self.write({
            'state': 'done',
            'holidays_to_post_ids': [(6, 0, hols.ids)],
            })
        action = self.env['ir.actions.act_window'].for_xml_id(
            'hr_holidays_usability', 'hr_holidays_post_action')
        action['res_id'] = self.id
        return action

    @api.multi
    def run(self):
        self.ensure_one()
        # I have to make a copy of self.holidays_to_post_ids in a variable
        # because, after the write, it doesn't have a value any more !!!
        holidays_to_post = self.holidays_to_post_ids
        today = fields.Date.context_today(self)
        if not self.holidays_to_post_ids:
            raise Warning(
                _('No leave request to post.'))
        self.holidays_to_post_ids.write({'posted_date': today})
        view_id = self.env.ref('hr_holidays_usability.hr_holiday_graph').id
        action = {
            'name': _('Leave Requests'),
            'res_model': 'hr.holidays',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', holidays_to_post.ids)],
            'view_mode': 'graph',
            'view_id': view_id,
            }
        return action
