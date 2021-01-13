# Copyright 2015-2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    _order = 'id desc'

    @api.model
    def get_stock_move_sold_out_report(self, move):
        lines = move.active_move_line_ids
        qty_in_lots = sum([x.product_uom_qty for x in lines])
        diff = round(move.product_qty - qty_in_lots, 3)
        if diff == 0.0:
            return ""
        return diff


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    code = fields.Char(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    product_tmpl_id = fields.Many2one(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    product_qty = fields.Float(track_visibility='onchange')
    product_uom_id = fields.Many2one(track_visibility='onchange')
    routing_id = fields.Many2one(track_visibility='onchange')
    ready_to_produce = fields.Selection(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
