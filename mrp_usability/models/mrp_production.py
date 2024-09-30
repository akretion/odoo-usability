# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models, Command


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    lot_producing_id = fields.Many2one(tracking=True)
    location_src_id = fields.Many2one(tracking=True)
    location_dest_id = fields.Many2one(tracking=True)
    bom_id = fields.Many2one(tracking=True)

    # Target: allow to modify location_dest_id until the button 'Mark as done' is pushed
    # I didn't find a better implementation... feel free to improve if you find one
    def _compute_move_finished_ids(self):
        for prod in self:
            if prod.state not in ('draft', 'done') and prod.location_dest_id:
                vals = {'location_dest_id': prod.location_dest_id.id}
                prod.move_finished_ids = [
                    Command.update(m.id, vals) for m in prod.move_finished_ids
                    if m.state != 'done'
                    ]
        super()._compute_move_finished_ids()

    # Method used by the report, inherited in this module
    # @api.model
    # def get_stock_move_sold_out_report(self, move):
    #    lines = move.active_move_line_ids
    #    qty_in_lots = sum([x.product_uom_qty for x in lines])
    #    diff = round(move.product_qty - qty_in_lots, 3)
    #    if diff == 0.0:
    #        return ""
    #    return diff
