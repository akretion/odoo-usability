# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleConfirm(models.TransientModel):
    _name = 'sale.confirm'
    _description = 'Wizard to confirm a sale order'

    sale_id = fields.Many2one(
        'sale.order', string='Sale Order', readonly=True)
    client_order_ref = fields.Char(string='Customer PO Number')
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Terms')
    partner_invoice_id = fields.Many2one(
        'res.partner', 'Invoice Address', required=True)
    show_partner_invoice_id = fields.Many2one(
        related='partner_invoice_id', readonly=True,
        string='Detailed Invoice Address')
    partner_shipping_id = fields.Many2one(
        'res.partner', 'Delivery Address', required=True)
    show_partner_shipping_id = fields.Many2one(
        related='partner_shipping_id', readonly=True,
        string='Detailed Delivery Address')

    @api.model
    def _prepare_default_get(self, order):
        default = {
            'sale_id': order.id,
            'client_order_ref': order.client_order_ref,
            'payment_term_id': order.payment_term_id.id or False,
            'partner_invoice_id': order.partner_invoice_id.id,
            'partner_shipping_id': order.partner_shipping_id.id,
        }
        return default

    @api.model
    def default_get(self, fields):
        res = super(SaleConfirm, self).default_get(fields)
        assert self._context.get('active_model') == 'sale.order',\
            'active_model should be sale.order'
        order = self.env['sale.order'].browse(self._context.get('active_id'))
        default = self._prepare_default_get(order)
        res.update(default)
        return res

    @api.multi
    def _prepare_update_so(self):
        self.ensure_one()
        return {
            'client_order_ref': self.client_order_ref,
            'payment_term_id': self.payment_term_id.id or False,
            'partner_invoice_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            }

    @api.multi
    def confirm(self):
        self.ensure_one()
        vals = self._prepare_update_so()
        self.sale_id.write(vals)
        # confirm sale order
        self.sale_id.action_confirm()
        return True
