# Copyright 2024 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    show_src_location = fields.Boolean(compute="_compute_show_location")
    show_dest_location = fields.Boolean(compute="_compute_show_location")

    @api.depends("picking_type_id.code", "location_id", "location_dest_id")
    def _compute_show_location(self):
        for picking in self:
            picking.show_src_location = (
                picking.picking_type_id.code != "incoming"
                and picking.location_id.child_ids
                )
            picking.show_dest_location = (
                picking.picking_type_id.code != "outgoing"
                and picking.location_dest_id.child_ids
                )
