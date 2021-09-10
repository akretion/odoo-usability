# Copyright 2015-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_type_id = fields.Many2one(tracking=True)
    incoterm_id = fields.Many2one(tracking=True)
    picking_status = fields.Selection([
        ('received', 'Fully Received'),
        ('partially_received', 'Partially Received'),
        ('to_receive', 'To Receive'),
        ('cancel', 'Receipt Cancelled'),
        ('no', 'Nothing to Receive')
        ], string='Picking Status', compute='_compute_picking_status',
        store=True)

    @api.depends('state', 'picking_ids.state')
    def _compute_picking_status(self):
        """
        Compute the picking status for the PO. Possible statuses:
        - no: if the PO is not in status 'purchase' nor 'done', we consider that
          there is nothing to receive. This is also the default value if the
          conditions of no other status is met.
        - cancel: all pickings are cancelled
        - received: if all  pickings are done or cancel.
        - partially_received: If at least one picking is done.
        - to_receive: if all pickings are in confirmed, assigned, waiting or
          cancel state.
        """
        for order in self:
            picking_status = 'no'
            if order.state in ('purchase', 'done') and order.picking_ids:
                pstates = [
                    picking.state for picking in order.picking_ids]
                if all([state == 'cancel' for state in pstates]):
                    picking_status = 'cancel'
                elif all([state in ('done', 'cancel') for state in pstates]):
                    picking_status = 'received'
                elif any([state == 'done' for state in pstates]):
                    picking_status = 'partially_received'
                elif all([
                        state in ('confirmed', 'assigned', 'waiting', 'cancel')
                        for state in pstates]):
                    picking_status = 'to_receive'
            order.picking_status = picking_status

    # inherit compute method of the field delivery_partner_id
    # defined in purchase_usability
    @api.depends('dest_address_id', 'picking_type_id')
    def _compute_delivery_partner_id(self):
        for o in self:
            delivery_partner_id = False
            if o.dest_address_id:
                delivery_partner_id = o.dest_address_id
            elif (
                    o.picking_type_id.warehouse_id and
                    o.picking_type_id.warehouse_id.partner_id):
                delivery_partner_id = o.picking_type_id.warehouse_id.partner_id
            o.delivery_partner_id = delivery_partner_id
