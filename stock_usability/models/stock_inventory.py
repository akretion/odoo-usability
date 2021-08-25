# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    product_barcode = fields.Char(related='product_id.barcode', string="Product Barcode")
