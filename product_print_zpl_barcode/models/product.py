# Copyright 2020-2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from stdnum.ean import calc_check_digit, is_valid
from barcode import EAN13, EAN8
from barcode.writer import ImageWriter
import base64
import io


class ProductTemplate(models.Model):
    _inherit = "product.template"

    must_print_barcode = fields.Boolean(
        string="Must Print Barcode",
        help="Enable that option for products for which you must "
        "print a barcode upon reception in stock.")

    def generate_barcode_from_product_template(self):
        self.ensure_one()
        if self.product_variant_count != 1:
            raise UserError(_(
                "You cannot call the method "
                "generate_barcode_from_product_template on product '%s' "
                "because it has %d variants and not just one.")
                % (self.display_name, self.product_variant_count))
        return self.product_variant_ids[0].generate_barcode_from_product_product()

    def print_zpl_barcode_from_product_template(self):
        self.ensure_one()
        if self.product_variant_count != 1:
            raise UserError(_(
                "You cannot call the method "
                "print_zpl_barcode_from_product_template on product '%s' "
                "because it has %d variants and not just one.")
                % (self.display_name, self.product_variant_count))
        action = self.env["ir.actions.actions"]._for_xml_id(
            'product_print_zpl_barcode.product_print_zpl_barcode_action')
        action['context'] = {
            'active_id': self.product_variant_ids[0].id,
            'active_model': 'product.product',
            }
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Not useful for ZPL, but it is often useful to have a barcode image field
    barcode_image = fields.Binary(
        compute='_compute_barcode_image',
        string='Barcode Image')

    @api.depends('barcode')
    def _compute_barcode_image(self):
        for product in self:
            barcode = product.barcode
            barcode_image = False
            if barcode:
                barcode_obj = False
                if len(barcode) == 13 and is_valid(barcode):
                    barcode_obj = EAN13(barcode, writer=ImageWriter(), guardbar=True)
                elif len(barcode) == 8 and is_valid(barcode):
                    barcode_obj = EAN8(barcode, writer=ImageWriter(), guardbar=True)
                if barcode_obj:
                    barcode_file = io.BytesIO()
                    barcode_obj.write(barcode_file)  # generate PNG
                    barcode_file.seek(0)
                    barcode_img = barcode_file.read()
                    barcode_image = base64.b64encode(barcode_img)
            product.barcode_image = barcode_image

    def generate_barcode_from_product_product(self):
        self.ensure_one()
        if self.barcode:
            raise UserError(_(
                "The product '%s' already has a barcode.") % self.display_name)
        barcode_without_checksum = self.env['ir.sequence'].next_by_code(
            'private.product.barcode')
        if len(barcode_without_checksum) not in (7, 12):
            raise UserError(_(
                "The sequence 'private.product.barcode' is not properly "
                "configured. The generated sequence should have 7 digits "
                "(for EAN-8) or 12 digits (for EAN-13). "
                "It currently has %d digits." % len(barcode_without_checksum)))
        checksum = calc_check_digit(barcode_without_checksum)
        barcode = barcode_without_checksum + str(checksum)
        self.write({
            'barcode': barcode,
            'must_print_barcode': True,
            })
