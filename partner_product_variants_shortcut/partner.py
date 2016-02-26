# -*- coding: utf-8 -*-
##############################################################################
#
#    Partner Product Variants Shortcut module for Odoo
#    Copyright (C) 2014-2016 Akretion (http://www.akretion.com)
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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _product_supplied_count(self):
        try:
            sellers = self.env['product.supplierinfo'].search(
                [('name', '=', self.id)])
            pproducts = self.env['product.product'].search(
                [('seller_ids', 'in', sellers.ids)])
            self.product_supplied_count = len(pproducts)
        except:
            pass

    product_supplied_count = fields.Integer(
        compute='_product_supplied_count', string="# of Products Supplied",
        readonly=True)
