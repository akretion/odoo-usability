# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    location_dest_list = fields.Text(
        string="Locations", compute="_compute_locations_dest_list"
    )

    @api.depends(
        "move_line_ids", "move_line_ids.location_dest_id", "move_line_ids.qty_done"
    )
    def _compute_locations_dest_list(self):
        for move in self:
            data = []
            separator = ", "
            dest_list = move.move_line_ids.location_dest_id
            for dest in dest_list:
                lines_qty = move.move_line_ids.search(
                    [("move_id", "=", move.id), ("location_dest_id", "=", dest.id)]
                ).mapped("qty_done")
                quantity = int(sum(lines_qty))
                location = dest.name
                data.append("{}: {}".format(quantity, location))
            move.location_dest_list = separator.join(data)

    def _compute_is_quantity_done_editable(self):
        super()._compute_is_quantity_done_editable()
        for move in self:
            if len(move.move_line_ids) == 1 and move.show_details_visible:
                move.is_quantity_done_editable = True
