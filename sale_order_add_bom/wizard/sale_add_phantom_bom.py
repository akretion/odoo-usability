# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import UserError
from openerp.tools import float_is_zero


class SaleAddPhantomBom(models.TransientModel):
    _name = 'sale.add.phantom.bom'
    _description = 'Add Kit to Quotation'

    @api.model
    def default_get(self, fields_list):
        res = super(SaleAddPhantomBom, self).default_get(fields_list)
        if self._context.get('active_model') == 'sale.order':
            res['sale_id'] = self._context['active_id']
        elif self._context.get('active_model') == 'stock.picking':
            res['picking_id'] = self._context['active_id']
        else:
            raise UserError(_(
                "The wizard can only be started from a sale order or a picking."))
        return res

    bom_id = fields.Many2one(
        'mrp.bom', 'Kit', required=True,
        domain=[('type', '=', 'phantom'), ('sale_ok', '=', True)])
    qty = fields.Integer(
        string='Number of Kits to Add', default=1, required=True)
    sale_id = fields.Many2one(
        'sale.order', string='Quotation')
    picking_id = fields.Many2one(
        'stock.picking', string='Picking')

    @api.model
    def _prepare_sale_order_line(self, bom_line, sale_order, wizard_qty):
        qty_in_product_uom = bom_line.product_uom_id._compute_quantity(
            bom_line.product_qty,
            bom_line.product_id.uom_id)
        vals = {
            'product_id': bom_line.product_id.id,
            'product_uom_qty': qty_in_product_uom * wizard_qty,
            'order_id': sale_order.id,
            }
        # on sale.order.line, company_id is a related field
        return vals

    @api.model
    def _prepare_stock_move(self, bom_line, picking, wizard_qty):
        product = bom_line.product_id
        qty_in_product_uom = bom_line.product_uom_id._compute_quantity(
            bom_line.product_qty, product.uom_id)
        vals = {
            'product_id': product.id,
            'product_uom_qty': qty_in_product_uom * wizard_qty,
            'product_uom': product.uom_id.id,
            'picking_id': picking.id,
            'company_id': picking.company_id.id,
            'location_id': picking.location_id.id,
            'location_dest_id': picking.location_dest_id.id,
            'name': product.partner_ref,
            }
        return vals

    @api.multi
    def add(self):
        self.ensure_one()
        assert self.sale_id or self.picking_id, 'No related sale_id or picking_id'
        if self.qty < 1:
            raise UserError(_(
                "The number of kits to add must be 1 or superior"))
        assert self.bom_id.type == 'phantom', 'The BOM is not a kit'
        if not self.bom_id.bom_line_ids:
            raise UserError(_("The selected kit is empty !"))
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        solo = self.env['sale.order.line']
        smo = self.env['stock.move']
        for line in self.bom_id.bom_line_ids:
            if float_is_zero(line.product_qty, precision_digits=prec):
                continue
            # The onchange is played in the inherit of the create()
            # of sale order line in the 'sale' module
            # TODO: if needed, we could increment existing order lines
            # with the same product instead of always creating new lines
            if self.sale_id:
                vals = self._prepare_sale_order_line(line, self.sale_id, self.qty)
                solo.create(vals)
            elif self.picking_id:
                vals = self._prepare_stock_move(line, self.picking_id, self.qty)
                smo.create(vals)
        return True
