# Copyright (C) 2021 Akretion (<http://www.akretion.com>).
# @author Kévin Roche <kevin.roche@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_fill_quantity_done(self):
        self.ensure_one()
        for move in self.move_ids_without_package:
            if move.move_line_ids:
                first_line = move.move_line_ids[0]
            else:
                first_line = False
            if move.quantity_done == 0 and first_line:
                qty = move.product_uom_qty
                if first_line.qty_done == 0:
                    first_line.write(
                        {
                            "qty_done": qty,
                        }
                    )
            elif move.quantity_done < move.product_uom_qty or (
                move.quantity_done == 0 and not first_line
            ):
                qty = move.product_uom_qty - move.quantity_done
                self.env["stock.move.line"].create(
                    {
                        "move_id": move.id,
                        "location_dest_id": move.location_dest_id.id,
                        "location_id": move.location_id.id,
                        "product_uom_id": move.product_uom.id,
                        "qty_done": qty,
                    }
                )
