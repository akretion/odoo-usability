# Copyright 2015-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare, float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(tracking=True)
    incoterm = fields.Many2one(tracking=True)
    picking_status = fields.Selection([
        ('delivered', 'Fully Delivered'),
        ('partially_delivered', 'Partially Delivered'),
        ('to_deliver', 'To Deliver'),
        ('cancel', 'Delivery Cancelled'),
        ('no', 'Nothing to Deliver')
        ], string='Picking Status', compute='_compute_picking_status',
        store=True)

    @api.depends('state', 'picking_ids.state')
    def _compute_picking_status(self):
        """
        Compute the picking status for the SO. Possible statuses:
        - no: if the SO is not in status 'sale' nor 'done', we consider that
          there is nothing to deliver. This is also the default value if the
          conditions of no other status is met.
        - cancel: all pickings are cancelled
        - delivered: if all  pickings are done or cancel.
        - partially_delivered: If at least one picking is done.
        - to_deliver: if all pickings are in confirmed, assigned, waiting or
          cancel state.
        """
        for order in self:
            picking_status = 'no'
            if order.state in ('sale', 'done') and order.picking_ids:
                pstates = [
                    picking.state for picking in order.picking_ids]
                if all([state == 'cancel' for state in pstates]):
                    picking_status = 'cancel'
                elif all([state in ('done', 'cancel') for state in pstates]):
                    picking_status = 'delivered'
                elif any([state == 'done' for state in pstates]):
                    picking_status = 'partially_delivered'
                elif all([
                        state in ('confirmed', 'assigned', 'waiting', 'cancel')
                        for state in pstates]):
                    picking_status = 'to_deliver'
            order.picking_status = picking_status

    def report_qty_to_deliver(self):
        # Can be useful for delivery report
        self.ensure_one()
        res = []
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self.order_line:
            if (
                    line.product_id.type in ('product', 'consu') and
                    float_compare(
                        line.product_uom_qty, line.qty_delivered,
                        precision_digits=prec) > 0):
                qty_to_deliver = float_round(
                    line.product_uom_qty - line.qty_delivered, precision_digits=prec)
                res.append({
                    'product': line.product_id,
                    'name': line.name,
                    'uom': line.product_uom,
                    'qty_to_deliver': qty_to_deliver,
                    })
        return res
