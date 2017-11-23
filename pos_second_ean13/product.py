# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    second_barcode = fields.Char(
        string='Second Barcode', copy=False, oldname='second_ean13',
        help='If the same product is available with two barcodes, you can '
        'enter a second barcode in this field')

    # TODO
    # The constrain below is "stupid" because you can have the same
    # value in 'barcode' field of product A and second_barcode of product B
    _sql_constraints = [(
        'second_barcode_unique',
        'unique(second_barcode)',
        'This barcode already exists!')]

    @api.constrains('second_barcode')
    def _check_second_barcode(self):
        for product in self:
            if product.second_barcode and not product.barcode:
                raise ValidationError(_(
                    "You should use the second barcode field only when "
                    "there is already a value in the main barcode field"))
