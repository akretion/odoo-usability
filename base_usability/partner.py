# -*- encoding: utf-8 -*-
##############################################################################
#
#    Base Usability module for Odoo
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

from openerp import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    ref = fields.Char(track_visibility='onchange', copy=False)
    lang = fields.Selection(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    vat = fields.Char(track_visibility='onchange')
    customer = fields.Boolean(track_visibility='onchange')
    supplier = fields.Boolean(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    street = fields.Char(track_visibility='onchange')
    street2 = fields.Char(track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    city = fields.Char(track_visibility='onchange')
    state_id = fields.Many2one(track_visibility='onchange')
    country_id = fields.Many2one(track_visibility='onchange')
    email = fields.Char(track_visibility='onchange')
    is_company = fields.Boolean(track_visibility='onchange')
    use_parent_address = fields.Boolean(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    # For reports
    name_title = fields.Char(
        compute='_compute_name_title', string='Name with Title')

    @api.one
    @api.depends('name', 'title', 'is_company')
    def _compute_name_title(self):
        name_title = self.name
        if self.title:
            title = self.title.shortcut or self.title.name
            if self.is_company:
                name_title = ' '.join([name_title, title])
            else:
                name_title = ' '.join([title, name_title])
        self.name_title = name_title


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    name = fields.Char(translate=False)
