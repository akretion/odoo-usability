# -*- coding: utf-8 -*-
##############################################################################
#
#    HR Usability module for Odoo
#    Copyright (C) 2016 Akretion (http://www.akretion.com)
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

from openerp import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    country_id = fields.Many2one(track_visibility='onchange')
    birthday = fields.Date(track_visibility='onchange')
    ssnid = fields.Char(track_visibility='onchange')
    sinid = fields.Char(track_visibility='onchange')
    identification_id = fields.Char(track_visibility='onchange')
    otherid = fields.Char(track_visibility='onchange')
    gender = fields.Selection(track_visibility='onchange')
    marital = fields.Selection(track_visibility='onchange')
    department_id = fields.Many2one(track_visibility='onchange')
    address_id = fields.Many2one(track_visibility='onchange')
    address_home_id = fields.Many2one(track_visibility='onchange')
    work_phone = fields.Char(track_visibility='onchange')
    mobile_phone = fields.Char(track_visibility='onchange')
    work_email = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    coach_id = fields.Many2one(track_visibility='onchange')
    job_id = fields.Many2one(track_visibility='onchange')
    passport_id = fields.Char(track_visibility='onchange')
