# Copyright 2015-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(track_visibility='onchange')
    incoterm = fields.Many2one(track_visibility='onchange')
    picking_status = fields.Selection([
        ('deliverd', 'Fully Deliverd'),
        ('partialy_delivered', 'Partialy Delivered'),
        ('to_deliver', 'To Deliver'),
        ('no', 'Nothing to Deliver')
        ], string='Picking Status', compute='_get_delivered', store=True, readonly=True)

    @api.depends('state', 'picking_ids.state')
    def _get_delivered(self):
        """
        Compute the picking status for the SO. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          deliver. This is also the default value if the conditions of no other status is met.
        - delivered: if all  pickings are done.
        - Partialy Done : If at least one picking is done.
        - To deliver : if all pickings are in confirmed, assigned or waiting state.
        """

        for order in self:

            if order.state not in ('sale', 'done') or not order.picking_ids:
                picking_status = 'no'
            elif all(picking.state == 'done' for picking in order.picking_ids):
                picking_status = 'deliverd'
            elif any(picking.state == 'done' for picking in order.picking_ids):
                picking_status = 'partialy_delivered'
            elif all(picking.state in ('confirmed', 'assigned', 'waiting') for picking in order.picking_ids):
                picking_status = 'to_deliver'
            else:
                picking_status = 'no'

            order.picking_status = picking_status
