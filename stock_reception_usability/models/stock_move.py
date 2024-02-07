# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from collections import defaultdict
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    location_dest_list = fields.Text(
        string="Dest. Locations", compute="_compute_locations_list"
    )

    location_src_list = fields.Text(
        string="Src. Locations", compute="_compute_locations_list"
    )

    @api.depends(
        "move_line_ids.location_dest_id",
        "move_line_ids.location_id",
        "move_line_ids.qty_done",
    )
    def _compute_locations_list(self):
        def format_loc(data):
            return "\n ".join([
                f"{int(qty) if qty.is_integer() else qty}: {location.name}"
                for location, qty in data.items()
                ])
        for move in self:
            dest = defaultdict(int)
            src = defaultdict(int)
            for line in move.move_line_ids:
                dest[line.location_dest_id] += line.qty_done
                src[line.location_id] += line.qty_done
            move.location_src_list = format_loc(src)
            move.location_dest_list = format_loc(dest)

    def _compute_is_quantity_done_editable(self):
        super()._compute_is_quantity_done_editable()
        for move in self:
            if len(move.move_line_ids) <= 1:
                move.is_quantity_done_editable = True
