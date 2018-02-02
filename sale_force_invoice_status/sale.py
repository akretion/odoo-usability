# -*- coding: utf-8 -*-
#  Copyright (C) 2018 Akretion (http://www.akretion.com)
#  @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def force_invoice_status_to_invoiced(self):
        for order in self:
            if order.state not in ('sale', 'done'):
                raise UserError(_(
                    "You are trying to force the sale order %s to invoiced "
                    "but it is not in 'Sales Order' or 'Locked' state.")
                    % order.name)
            if order.invoice_status != 'to invoice':
                raise UserError(_(
                    "You are trying to force the sale order %s to invoiced "
                    "but its invoice status is not 'To Invoice'.")
                    % order.name)
            order.order_line.write({'forced_to_invoiced': True})
            order.message_post(_(
                "Order <b>forced to Invoiced</b> via the special button"))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    forced_to_invoiced = fields.Boolean()

    @api.depends(
        'state', 'product_uom_qty', 'qty_delivered', 'qty_to_invoice',
        'qty_invoiced', 'forced_to_invoiced')
    def _compute_invoice_status(self):
        super(SaleOrderLine, self)._compute_invoice_status()
        for line in self:
            if line.state in ('sale', 'done') and line.forced_to_invoiced:
                line.invoice_status = 'invoiced'
