# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    # Field needed to be able to search on supplier in the "Replenish" tree view
    # I put it in purchase_stock_usability and not stock_usability
    # because I wanted to use the field 'show_supplier' defined in purchase_stock
    # (but I don't use it in the end because its computation returns False even
    # on products with a Buy route) and I may also
    # one day interact with supplier_id (M2O product.supplierinfo) defined in
    # purchase_stock
    seller_id = fields.Many2one(
        related='product_id.product_tmpl_id.seller_ids.name',
        store=True, string='Supplier',
        )
