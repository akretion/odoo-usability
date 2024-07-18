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

    _sql_constraints = [(
        # Maybe it could be better to have a constrain per company
        # but the company_id field is on product.template,
        # not on product.product
        # If it's a problem, we'll create a company_id field on
        # product.product
        'default_code_uniq',
        'unique(default_code)',
        'This internal reference already exists!')]

    @api.model
    def _get_barcode_type(self, barcode):
        barcode_type = False
        size2label = {
            8: 'EAN-8',
            13: 'EAN-13',
            14: 'GTIN-14',
            }
        if barcode:
            size = len(barcode)
            if size in size2label and is_valid(barcode):
                barcode_type = size2label[size]
        return barcode_type

    @api.depends('barcode')
    def _compute_barcode_type(self):
        for product in self:
            product.barcode_type = self._get_barcode_type(product.barcode)
