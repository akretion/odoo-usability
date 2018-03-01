# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    country_id = fields.Many2one(track_visibility='onchange')
    birthday = fields.Date(track_visibility='onchange')
    ssnid = fields.Char(track_visibility='onchange')
    sinid = fields.Char(track_visibility='onchange')
    identification_id = fields.Char(track_visibility='onchange')
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

    _sql_constraints = [
        ('identification_unique',
        'unique(identification_id)',
        'An employee with this Identification No already exists'),
        ('ssnid_unique',
        'unique(ssnid)',
        'An employee with this Social Security Number already exists'),
        ('sinid_unique',
        'unique(sinid)',
        'An employee with this Social Insurance Number already exists'),
        ('passport_id_unique',
        'unique(passport_id)',
        'An employee with this Passport No already exists'),
        ]
