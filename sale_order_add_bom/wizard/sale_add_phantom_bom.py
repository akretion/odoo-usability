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
    def _default_sale_id(self):
        assert self._context.get('active_model') == 'sale.order'
        return self.env['sale.order'].browse(self._context['active_id'])

    bom_id = fields.Many2one(
        'mrp.bom', 'Kit', required=True,
        domain=[('type', '=', 'phantom'), ('sale_ok', '=', True)])
    qty = fields.Integer(
        string='Number of Kits to Add', default=1, required=True)
    # I can 't put the sale_id fields required=True because
    # it may block the deletion of a sale order
    sale_id = fields.Many2one(
        'sale.order', string='Quotation', default=_default_sale_id)

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
        return vals

    @api.multi
    def add(self):
        self.ensure_one()
        assert self.sale_id, 'No related sale_id'
        if self.qty < 1:
            raise UserError(_(
                "The number of kits to add must be 1 or superior"))
        assert self.bom_id.type == 'phantom', 'The BOM is not a kit'
        if not self.bom_id.bom_line_ids:
            raise UserError(_("The selected kit is empty !"))
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        today = fields.Date.context_today(self)
        solo = self.env['sale.order.line']
        for line in self.bom_id.bom_line_ids:
            if float_is_zero(line.product_qty, precision_digits=prec):
                continue
            # The onchange is played in the inherit of the create()
            # of sale order line in the 'sale' module
            # TODO: if needed, we could increment existing order lines
            # with the same product instead of always creating new lines
            vals = self._prepare_sale_order_line(line, self.sale_id, self.qty)
            solo.create(vals)
        return True
