# -*- coding: utf-8 -*-
# © 2015 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    # Change product_tmpl_id to required=False
    # because I added that field to form view and it blocks when you save
    # the product form with a new supplier info
    # This field is now required in the form view
    product_tmpl_id = fields.Many2one(required=False)
