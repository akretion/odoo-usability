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

from openerp import models, fields


class CreditControlPolicyLevel(models.Model):
    _inherit = "credit.control.policy.level"
    _rec_name = 'internal_name'

    channel = fields.Selection(selection_add=[('phone', 'Phone call')])
    name = fields.Char(
        string='Subject',
        help="Will be displayed in the subject of the emails and in "
        "the letters")
    internal_name = fields.Char(string='Internal Name', required=True)


class CreditControlLine(models.Model):
    _inherit = "credit.control.line"

    channel = fields.Selection(selection_add=[('phone', 'Phone call')])
