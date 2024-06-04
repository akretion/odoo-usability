# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    # Fixing bug https://github.com/odoo/odoo/issues/34702
    @api.depends("product_id", "product_uom_qty", "product_uom")
    def _cal_move_weight(self):
        weight_uom_categ = self.env.ref("uom.product_uom_categ_kgm")
        kg_uom = self.env.ref("uom.product_uom_kgm")
        for move in self:
            if move.product_id.uom_id.category_id == weight_uom_categ:
                move.weight = move.product_id.uom_id._compute_quantity(
                    move.product_qty, kg_uom
                )
            else:
                move.weight = move.product_qty * move.product_id.weight
