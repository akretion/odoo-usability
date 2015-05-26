# -*- encoding: utf-8 -*-
##############################################################################
#
#    Procurement Suggest module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
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
import openerp.addons.decimal_precision as dp
from openerp.exceptions import Warning


class ProcurementSuggestionGenerate(models.TransientModel):
    _name = 'procurement.suggest.generate'
    _description = 'Start to generate the procurement suggestions'

    categ_id = fields.Many2one(
        'product.category', string='Product Category')
    seller_id = fields.Many2one(
        'res.partner', string='Supplier',
        domain=[('supplier', '=', True), ('is_company', '=', True)])
    location_id = fields.Many2one(
        'stock.location', string='Stock Location', required=True,
        default=lambda self: self.env.ref('stock.stock_location_stock'))

    @api.model
    def _prepare_suggest_line(self, orderpoint):
        porderline_id = False
        if orderpoint.product_id.seller_id:
            porderlines = self.env['purchase.order.line'].search([
                ('state', 'not in', ('draft', 'cancel')),
                ('product_id', '=', orderpoint.product_id.id)],
                order='id desc', limit=1)
            # I cannot filter on 'date_order' because it is not a stored field
            porderline_id = porderlines and porderlines[0].id or False
        sline = {
            'product_id': orderpoint.product_id.id,
            'seller_id': orderpoint.product_id.seller_id.id or False,
            'qty_available': orderpoint.product_id.qty_available,
            'incoming_qty': orderpoint.product_id.incoming_qty,
            'outgoing_qty': orderpoint.product_id.outgoing_qty,
            'orderpoint_id': orderpoint.id,
            'last_po_line_id': porderline_id,
            }
        return sline

    @api.multi
    def run(self):
        op_domain = [
            ('suggest', '=', True),
            ('company_id', '=', self.env.user.company_id.id),
            ('location_id', 'child_of', self.location_id.id),
            ]
        if self.categ_id or self.seller_id:
            product_domain = []
            if self.categ_id:
                product_domain.append(
                    ('categ_id', 'child_of', self.categ_id.id))
            if self.seller_id:
                product_domain.append(
                    ('seller_id', '=', self.seller_id.id))
            products = self.env['product.product'].search(product_domain)
            op_domain.append(('product_id', 'in', products.ids))
        self = self.with_context(location_id=self.location_id.id)
        ops = self.env['stock.warehouse.orderpoint'].search(op_domain)
        pso = self.env['procurement.suggest']
        p_suggest_lines = []
        lines = {}  # key = product_id ; value = {'min_qty', ...}
        for op in ops:
            if op.product_id.virtual_available < op.product_min_qty:
                if op.product_id.id in lines:
                    raise Warning(
                        _("There are 2 orderpoints (%s and %s) for the same "
                            "product on stock location %s or its "
                            "children.") % (
                            lines[op.product_id.id]['orderpoint'].name,
                            op.name,
                            self.location_id.complete_name))
                p_suggest_lines.append(self._prepare_suggest_line(op))
        p_suggest_lines_sorted = sorted(
            p_suggest_lines, key=lambda to_sort: to_sort['seller_id'])
        if p_suggest_lines_sorted:
            p_suggest_ids = []
            for p_suggest_line in p_suggest_lines_sorted:
                p_suggest = pso.create(p_suggest_line)
                p_suggest_ids.append(p_suggest.id)
            action = self.env['ir.actions.act_window'].for_xml_id(
                'procurement_suggest', 'procurement_suggest_action')
            action.update({
                'target': 'current',
                'domain': [('id', 'in', p_suggest_ids)],
            })
            return action
        else:
            raise Warning(_(
                "The virtual stock for all related products is above the "
                "minimum stock level."))


class ProcurementSuggest(models.TransientModel):
    _name = 'procurement.suggest'
    _description = 'Procurement Suggestions'
    _rec_name = 'product_id'

    product_id = fields.Many2one(
        'product.product', string='Product', required=True, readonly=True)
    seller_id = fields.Many2one(
        'res.partner', string='Supplier', readonly=True)
    qty_available = fields.Float(
        string='Quantity On Hand', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    incoming_qty = fields.Float(
        string='Incoming Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    outgoing_qty = fields.Float(
        string='Outgoing Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    last_po_line_id = fields.Many2one(
        'purchase.order.line', string='Last Purchase Order Line',
        readonly=True)
    last_po_date = fields.Datetime(
        related='last_po_line_id.order_id.date_order',
        string='Date of the last PO', readonly=True)
    last_po_qty = fields.Float(
        related='last_po_line_id.product_qty', readonly=True,
        string='Quantity of the Last Order')
    orderpoint_id = fields.Many2one(
        'stock.warehouse.orderpoint', string='Re-ordering Rule',
        readonly=True)
    min_qty = fields.Float(
        string="Min Quantity", readonly=True,
        related='orderpoint_id.product_min_qty',
        digits=dp.get_precision('Product Unit of Measure'))
    qty_to_order = fields.Float(
        string='Quantity to Order',
        digits=dp.get_precision('Product Unit of Measure'))


class ProcurementSuggestPoCreate(models.TransientModel):
    _name = 'procurement.suggest.po.create'
    _description = 'ProcurementSuggestPoCreate'

    @api.model
    def _prepare_purchase_order_vals(self, partner, po_lines):
        polo = self.pool['purchase.order.line']
        ponull = self.env['purchase.order'].browse(False)
        po_vals = {'partner_id': partner.id}
        partner_change_dict = ponull.onchange_partner_id(partner.id)
        po_vals.update(partner_change_dict['value'])
        picking_type_id = self.env['purchase.order']._get_picking_in()
        picking_type_dict = ponull.onchange_picking_type_id(picking_type_id)
        po_vals.update(picking_type_dict['value'])
        order_lines = []
        for product, qty_to_order in po_lines:
            product_change_res = polo.onchange_product_id(
                self._cr, self._uid, [],
                partner.property_product_pricelist_purchase.id,
                product.id, qty_to_order, False, partner.id,
                fiscal_position_id=partner.property_account_position.id,
                context=self.env.context)
            product_change_vals = product_change_res['value']
            taxes_id_vals = []
            if product_change_vals.get('taxes_id'):
                for tax_id in product_change_vals['taxes_id']:
                    taxes_id_vals.append((4, tax_id))
                product_change_vals['taxes_id'] = taxes_id_vals
            order_lines.append(
                [0, 0, dict(product_change_vals, product_id=product.id)])
        po_vals['order_line'] = order_lines
        return po_vals

    @api.multi
    def create_po(self):
        self.ensure_one()
        # group by supplier
        po_to_create = {}  # key = seller_id, value = [(product, qty)]
        psuggest_ids = self.env.context.get('active_ids')
        for line in self.env['procurement.suggest'].browse(psuggest_ids):
            if not line.qty_to_order:
                continue
            if line.seller_id in po_to_create:
                po_to_create[line.seller_id].append(
                    (line.product_id, line.qty_to_order))
            else:
                po_to_create[line.seller_id] = [
                    (line.product_id, line.qty_to_order)]
        new_po_ids = []
        for seller, po_lines in po_to_create.iteritems():
            po_vals = self._prepare_purchase_order_vals(
                seller, po_lines)
            new_po = self.env['purchase.order'].create(po_vals)
            new_po_ids.append(new_po.id)

        if not new_po_ids:
            raise Warning(_('No purchase orders created'))
        action = self.env['ir.actions.act_window'].for_xml_id(
            'purchase', 'purchase_rfq')
        action.update({
            'nodestroy': False,
            'target': 'current',
            'domain': [('id', 'in', new_po_ids)],
            })
        return action
