# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Date Planned Update module for Odoo
#    Copyright (C) 2015-2016 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp


class PurchaseDatePlannedUpdate(models.TransientModel):
    _name = 'purchase.date.planned.update'
    _description = 'Update Scheduled Date on PO'

    date_planned = fields.Date(string='New Scheduled Date For All Lines')
    line_ids = fields.One2many(
        'purchase.line.date.planned.update', 'parent_id', string="Lines")

    @api.model
    def default_get(self, fields):
        res = super(PurchaseDatePlannedUpdate, self).default_get(fields)
        po = self.env['purchase.order'].browse(self._context['active_id'])
        lines = []
        for line in po.order_line:
            if line.move_ids:
                if all([move.state == 'done' for move in line.move_ids]):
                    continue
            lines.append({
                'purchase_line_id': line.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_qty': line.product_qty,
                'date_planned': line.date_planned,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                })
        if not lines:
            raise UserError(_(
                "All purchase order lines have been fully received."))
        res.update(line_ids=lines)
        return res

    @api.onchange('date_planned')
    def date_planned_change(self):
        if self.date_planned:
            for line in self.line_ids:
                line.date_planned = self.date_planned

    @api.multi
    def run(self):
        self.ensure_one()
        for wline in self.line_ids:
            if wline.date_planned != wline.purchase_line_id.date_planned:
                pline = wline.purchase_line_id
                pline.order_id.message_post(_(
                    "Updated Scheduled Date of line <b>%s</b> from %s "
                    "to <b>%s</b>")
                    % (pline.name, pline.date_planned, wline.date_planned))
                # Update PO line
                pline.date_planned = wline.date_planned
                # Update move lines
                if pline.move_ids:
                    moves = pline.move_ids.filtered(
                        lambda x: x.state != 'done')
                    moves.write({'date_expected': wline.date_planned})
        return True


class PurchaseLineDatePlannedUpdate(models.TransientModel):
    _name = 'purchase.line.date.planned.update'
    _description = 'Purchase Line Date Planned Update'

    parent_id = fields.Many2one(
        'purchase.date.planned.update', string='Parent')
    purchase_line_id = fields.Many2one(
        'purchase.order.line', string='Purchase Order Line', readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product', readonly=True)
    name = fields.Text('Description', readonly=True)
    product_qty = fields.Float(
        string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        readonly=True)
    date_planned = fields.Date(string='Scheduled Date', required=True)
    product_uom = fields.Many2one(
        'product.uom', string='Product Unit of Measure', readonly=True)
    price_unit = fields.Float(
        string='Unit Price', readonly=True,
        digits=dp.get_precision('Product Price'))
