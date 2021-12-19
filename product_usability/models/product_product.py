# Copyright 2015-2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(copy=False, tracking=10)
    barcode = fields.Char(tracking=20)
    weight = fields.Float(tracking=30)
    active = fields.Boolean(tracking=40)
    barcode_code128 = fields.Char(
        compute='_compute_barcode_code128',
        help="Barcode in Code128-B with start char, checksum and stop char")

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
    def _compute_code128_checksum(self, code):
        # This is NOT a full implementation of code128 checksum
        csum = 104  # Start B
        i = 0
        for char in code:
            i += 1
            char_val = ord(char) - 32
            csum += char_val * i
        remainder = csum % 103
        checksum = chr(remainder + 32)
        return checksum

    @api.depends('barcode')
    def _compute_barcode_code128(self):
        # We use Code128-B. Useful info on code128:
        # https://boowiki.info/art/codes-a-barres/code-128.html
        # Use code128.ttf and copy it in /usr/local/share/fonts/
        startb = chr(209)
        stop = chr(211)
        for product in self:
            code128 = False
            barcode = product.barcode
            if barcode and all([32 <= ord(x) <= 127 for x in barcode]):
                checksum = self._compute_code128_checksum(barcode)
                if checksum:
                    code128 = startb + barcode + checksum + stop
            product.barcode_code128 = code128
