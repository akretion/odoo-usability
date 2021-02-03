# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from stdnum.ean import calc_check_digit


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
        action = self.env.ref(
            'product_print_zpl_barcode.product_print_zpl_barcode_action').sudo().read()[0]
        action['context'] = {
            'active_id': self.product_variant_ids[0].id,
            'active_model': 'product.product',
            }
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

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
