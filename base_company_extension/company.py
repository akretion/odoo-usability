# -*- coding: utf-8 -*-
##############################################################################
#
#    Base Company Extension module for Odoo
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

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    capital_amount = fields.Integer(string='Capital Amount')
    title = fields.Many2one(
        'res.partner.title', related='partner_id.title',
        string='Legal Form')

    _sql_constraints = [(
        'capital_amount_positive',
        'CHECK (capital_amount >= 0)',
        "The value of the field 'Capital Amount' must be positive."
        )]
