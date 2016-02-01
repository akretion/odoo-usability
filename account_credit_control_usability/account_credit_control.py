# -*- coding: utf-8 -*-
##############################################################################
#
#    Account Credit Control Usability module for Odoo
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


class CreditControlPolicyLevel(models.Model):
    _inherit = "credit.control.policy.level"
    _rec_name = 'internal_name'

    channel = fields.Selection(selection_add=[('phone', 'Phone Call')])
    name = fields.Char(
        string='Subject',
        help="Will be displayed in the subject of the emails and in "
        "the letters")
    internal_name = fields.Char(string='Internal Name', required=True)


class CreditControlLine(models.Model):
    _inherit = "credit.control.line"

    channel = fields.Selection(selection_add=[('phone', 'Phone Call')])

    @api.multi
    def open_aged_open_invoices_report(self):
        self.ensure_one()
        return self.partner_id.open_aged_open_invoices_report()

    @api.multi
    def go_to_partner_form(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'base', 'action_partner_customer_form')
        action.update({
            'view_mode': 'form,kanban,tree',
            'views': False,
            'res_id': self.partner_id.id,
            'context': {},
        })
        return action


class CreditControlRun(models.Model):
    _inherit = "credit.control.run"

    date = fields.Date(default=fields.Date.context_today)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('credit_control_line_ids')
    def _credit_control_line_count(self):
        try:
            self.credit_control_line_count = len(self.credit_control_line_ids)
        except:
            self.credit_control_line_count = 0

    credit_control_line_count = fields.Integer(
        compute='_credit_control_line_count',
        string="# of Credit Control Lines", readonly=True)
