# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Usability Extension module for Odoo
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

from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(track_visibility='onchange')
    date_order = fields.Datetime(track_visibility='onchange')
    date_confirm = fields.Date(track_visibility='onchange')
    client_order_ref = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    partner_shipping_id = fields.Many2one(track_visibility='onchange')
    partner_invoice_id = fields.Many2one(track_visibility='onchange')
    pricelist_id = fields.Many2one(track_visibility='onchange')
    order_policy = fields.Selection(track_visibility='onchange')
    payment_term = fields.Many2one(track_visibility='onchange')
    fiscal_position = fields.Many2one(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
