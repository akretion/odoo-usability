# Copyright 2018-2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    # product.packaging is defined in the 'product' module and enhanced in the 'delivery' module
    # I used to make the improvements on the datamodel of product.packaging in the OCA module
    # 'stock_packaging_usability_pp' from OCA/stock-logistics-tracking,
    # but I eventually figured out that the feature provided by 'stock_packaging_usability_pp'
    # was native in the 'delivery' module via the wizard choose.delivery.package.
    # So I stopped using 'stock_packaging_usability_pp' and I moved the datamodel changes
    # here in the module 'delivery_usability'
    name = fields.Char(translate=True)
    weight = fields.Float(digits="Stock Weight", string="Empty Package Weight")
    active = fields.Boolean(default=True)
    # packaging_type is important, in particular for pallets for which
    # we need a special implementation to enter the height
    packaging_type = fields.Selection(
        [
            ("unit", "Unit"),
            ("pack", "Pack"),
            ("box", "Box"),
            ("pallet", "Pallet"),
        ],
        string="Type",
    )
