# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    default_code = fields.Char(copy=False)
    #        track_visibility='onchange',

    #    barcode = fields.Char(track_visibility='onchange',

    #    weight = fields.Float(track_visibility='onchange')
    #    active = fields.Boolean(track_visibility='onchange')

    _sql_constraints = [
        (
            # Maybe it could be better to have a constrain per company
            # but the company_id field is on product.template,
            # not on product.product
            # If it's a problem, we'll create a company_id field on
            # product.product
            "default_code_uniq",
            "unique(default_code)",
            "This internal reference already exists!",
        )
    ]
