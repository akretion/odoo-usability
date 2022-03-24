# Copyright 2015-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    picking_type_id = fields.Many2one(tracking=True)
    incoterm_id = fields.Many2one(tracking=True)
    picking_status = fields.Selection(
        [
            ("received", "Fully Received"),
            ("partially_received", "Partially Received"),
            ("to_receive", "To Receive"),
            ("cancel", "Receipt Cancelled"),
            ("no", "Nothing to Receive"),
        ],
        string="Reception Status",
        compute="_compute_picking_status",
        store=True,
        default="no",
    )

    @api.depends("state", "picking_ids.state")
    def _compute_picking_status(self):
        for order in self:
            line_ids = order.order_line
            order.picking_status = line_ids.get_move_status()

    # inherit compute method of the field delivery_partner_id
    # defined in purchase_usability
    @api.depends("dest_address_id", "picking_type_id")
    def _compute_delivery_partner_id(self):
        for o in self:
            delivery_partner_id = False
            if o.dest_address_id:
                delivery_partner_id = o.dest_address_id
            elif (
                o.picking_type_id.warehouse_id
                and o.picking_type_id.warehouse_id.partner_id
            ):
                delivery_partner_id = o.picking_type_id.warehouse_id.partner_id
            o.delivery_partner_id = delivery_partner_id


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    move_status = fields.Selection(
        [
            ("received", "Fully Received"),
            ("partially_received", "Partially Received"),
            ("to_receive", "To Receive"),
            ("cancel", "Receipt Cancelled"),
            ("no", "Nothing to Receive"),
        ],
        string="Reception Status",
        compute="_compute_move_status",
        store=True,
        default="no",
    )

    def get_move_status(self):
        """
        Returns the reception status of the related lines stock moves.
        Possible statuses:
            - no: if the PO is not in status 'purchase' nor 'done', we consider that
              there is nothing to receive. This is also the default value if the
              conditions of no other status is met.
            - cancel: all stock moves are cancelled
            - received: if all stock moves are done or cancel.
            - partially_received: If at least one stock move is done.
            - to_receive: if all stock moves are in confirmed, assigned, waiting or
              cancel state.
        """
        move_status = "no"
        mstates = self.move_ids.mapped("state")

        if all([state == "cancel" for state in mstates]):
            move_status = "cancel"
        elif all([state in ("done", "cancel") for state in mstates]):
            move_status = "received"
        elif any([state == "done" for state in mstates]):
            move_status = "partially_received"
        elif all(
            [
                state in ("confirmed", "assigned", "waiting", "cancel")
                for state in mstates
            ]
        ):
            move_status = "to_receive"
        return move_status

    @api.depends("state", "move_ids.state")
    def _compute_move_status(self):
        for line in self:
            line.move_status = line.get_move_status()
