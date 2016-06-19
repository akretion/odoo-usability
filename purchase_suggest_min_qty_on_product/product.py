# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Suggest Min Qty on Product module for Odoo
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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp
from openerp.tools import float_compare, float_is_zero
from openerp.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    min_qty = fields.Float(
        string=u'Minimum Quantity', track_visibility='onchange',
        digits=dp.get_precision('Product Unit of Measure'),
        company_dependent=True,
        help="If the forecast quantity is lower than the value of this field, "
        "Odoo will suggest to re-order this product. This field is in the "
        "unit of measure of the product.")
    max_qty = fields.Float(
        string=u'Maximum Quantity', track_visibility='onchange',
        digits=dp.get_precision('Product Unit of Measure'),
        company_dependent=True,
        help="If the forecast quantity is lower than the value of the minimum "
        " quantity, Odoo will suggest to re-order this product to go up to "
        "the maximum quantity. This field is in the unit of measure of the "
        "product.")

    @api.constrains('min_qty', 'max_qty')
    def check_min_max_qty(self):
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for product in self:
            if (
                    not float_is_zero(
                        product.max_qty, precision_digits=precision) and
                    float_compare(
                        product.max_qty, product.min_qty,
                        precision_digits=precision) != 1):
                raise ValidationError(_(
                    "On product '%s', the maximum quantity (%s) is lower "
                    "than the minimum quantity (%s).") % (
                    product.name_get()[0][1],
                    product.max_qty, product.min_qty))
