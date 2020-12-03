# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Method used by the report, inherited in this module
    @api.model
    def get_stock_move_sold_out_report(self, move):
        lines = move.active_move_line_ids
        qty_in_lots = sum([x.product_uom_qty for x in lines])
        diff = round(move.product_qty - qty_in_lots, 3)
        if diff == 0.0:
            return ""
        return diff
