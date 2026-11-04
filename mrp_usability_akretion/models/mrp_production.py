# Copyright 2015-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models
from odoo.tools import float_round


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    lot_producing_id = fields.Many2one(tracking=True)
    location_src_id = fields.Many2one(tracking=True)
    location_dest_id = fields.Many2one(tracking=True)
    bom_id = fields.Many2one(tracking=True)

    # Target: allow to modify location_dest_id until the button 'Mark as done' is pushed
    # I didn't find a better implementation... feel free to improve if you find one
    def _compute_move_finished_ids(self):
        for prod in self:
            if prod.state not in ("draft", "done") and prod.location_dest_id:
                vals = {"location_dest_id": prod.location_dest_id.id}
                prod.move_finished_ids = [
                    Command.update(m.id, vals)
                    for m in prod.move_finished_ids
                    if m.state != "done"
                ]
        super()._compute_move_finished_ids()

    # Method used by the report
    @api.model
    def get_stock_move_sold_out_report(self, move):
        sml_qties = sum([x.quantity_product_uom for x in move.move_line_ids])
        diff = float_round(
            move.product_uom_qty - sml_qties,
            precision_rounding=move.product_uom.rounding,
        )
        if diff == 0.0:
            return ""
        return diff
