# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Allow to change the destination location until 'Mark as done'.
    # Native behavior: it is only possible to change it in draft state.
    location_dest_id = fields.Many2one(states={
        'draft': [('readonly', False)],      # native
        'confirmed': [('readonly', False)],  # added
        'progress': [('readonly', False)],   # added
        'to_close': [('readonly', False)],   # added
        }, tracking=True)
    # Add field product_categ_id for reporting only
    product_categ_id = fields.Many2one(related='product_id.categ_id', store=True)
    lot_producing_id = fields.Many2one(tracking=True)
    location_src_id = fields.Many2one(tracking=True)
    location_dest_id = fields.Many2one(tracking=True)
    bom_id = fields.Many2one(tracking=True)

    # Method used by the report, inherited in this module
    @api.model
    def get_stock_move_sold_out_report(self, move):
        lines = move.active_move_line_ids
        qty_in_lots = sum([x.product_uom_qty for x in lines])
        diff = round(move.product_qty - qty_in_lots, 3)
        if diff == 0.0:
            return ""
        return diff
