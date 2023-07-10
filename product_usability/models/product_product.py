# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from stdnum.ean import is_valid


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(copy=False, tracking=10)
    barcode = fields.Char(tracking=20)
    weight = fields.Float(tracking=30)
    active = fields.Boolean(tracking=40)
    barcode_type = fields.Char(compute='_compute_barcode_type')

    @api.model
    def _get_barcode_type(self, barcode):
        barcode_type = False
        if barcode:
            size = len(barcode)
            if size == 13 and is_valid(barcode):
                barcode_type = 'EAN13'
            elif size == 8 and is_valid(barcode):
                barcode_type = 'EAN8'
        return barcode_type

    @api.depends('barcode')
    def _compute_barcode_type(self):
        for product in self:
            product.barcode_type = self._get_barcode_type(product.barcode)
