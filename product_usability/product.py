# -*- coding: utf-8 -*-
##############################################################################
#
#    Product Usability module for Odoo
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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_history_ids = fields.One2many(
        'product.price.history', 'product_template_id',
        string='Product Price History')
    name = fields.Char(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    categ_id = fields.Many2one(track_visibility='onchange')
    list_price = fields.Float(track_visibility='onchange')
    sale_ok = fields.Boolean(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    state = fields.Selection(track_visibility='onchange')
    weight = fields.Float(track_visibility='onchange')
    weight_net = fields.Float(track_visibility='onchange')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(track_visibility='onchange')
    ean13 = fields.Char(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
