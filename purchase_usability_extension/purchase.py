# -*- coding: utf-8 -*-
# © 2015-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    _order = 'order_id, sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    dest_address_id = fields.Many2one(track_visibility='onchange')
    pricelist_id = fields.Many2one(track_visibility='onchange')
    date_approve = fields.Date(track_visibility='onchange')
    validator = fields.Many2one(track_visibility='onchange')
    invoice_method = fields.Selection(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position = fields.Many2one(track_visibility='onchange')
    incoterm_id = fields.Many2one(track_visibility='onchange')
    partner_ref = fields.Char(track_visibility='onchange')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Field added to have a clickable link from picking to PO
    purchase_id = fields.Many2one(
        related='move_lines.purchase_line_id.order_id', readonly=True,
        string='Purchase Order')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    def _purchase_stats(self):
        poo = self.env['purchase.order']
        aio = self.env['account.invoice']
        try:
            self.purchase_order_count = poo.search_count(
                [('partner_id', 'child_of', self.id)])
        except:
            pass
        try:
            self.supplier_invoice_count = aio.search_count([
                ('partner_id', 'child_of', self.id),
                ('type', '=', 'in_invoice')])
        except:
            pass

    # Fix an access right issue when accessing partner form without being
    # a member of the purchase/User group
    purchase_order_count = fields.Integer(
        compute='_purchase_stats', string='# of Purchase Order')
    supplier_invoice_count = fields.Integer(
        compute='_purchase_stats', string='# Supplier Invoices')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    purchase_ok = fields.Boolean(track_visibility='onchange')
