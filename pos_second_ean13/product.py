# -*- coding: utf-8 -*-
##############################################################################
#
#    POS Second EAN13 module for Odoo
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

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from openerp.addons.product.product import check_ean


class ProductProduct(models.Model):
    _inherit = 'product.product'

    second_ean13 = fields.Char(
        string='Second EAN13 Barcode', size=13,
        help='If the same product is available with two EAN13, you can enter '
        'a second EAN13 in this field')

    @api.multi
    @api.constrains('second_ean13')
    def _check_second_ean13(self):
        for product in self:
            if product.second_ean13:
                if not product.ean13:
                    raise ValidationError(_(
                        "You should use the second EAN13 field only when "
                        "there is already a value in the main EAN13 field"))
                if not check_ean(product.second_ean13):
                    raise ValidationError(_(
                        "The second EAN13 barcode is invalid."))
