# -*- coding: utf-8 -*-
##############################################################################
#
#    Project Issue Extension module for Odoo
#    Copyright (C) 2014-2015 Akretion (http://www.akretion.com)
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


class ProjectIssue(models.Model):
    _inherit = 'project.issue'
    _rec_name = 'display_name'

    @api.multi
    @api.depends('number', 'name')
    def compute_display_name(self):
        for issue in self:
            issue.display_name = u'[%s] %s' % (issue.number, issue.name)

    number = fields.Char(string='Number', copy=False, default='/')
    display_name = fields.Char(
        compute='compute_display_name', string='Display Name', store=True)
    target_date = fields.Datetime(
        string='Target Resolution Date', track_visibility='onchange')
    product_ids = fields.Many2many(
        'product.product', string="Related Products")

    @api.model
    def create(self, vals):
        if vals.get('number', '/'):
            vals['number'] = self.env['ir.sequence'].next_by_code(
                'project.issue')
        return super(ProjectIssue, self).create(vals)

    _sql_constraints = [(
        'number_company_uniq',
        'unique(number, company_id)',
        'An issue with the same number already exists for this company !'
        )]
