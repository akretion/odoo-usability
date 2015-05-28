# -*- encoding: utf-8 -*-
##############################################################################
#
#    Purchase Suggest module for Odoo
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
from openerp.tools import float_compare
from openerp.exceptions import Warning
import logging

logger = logging.getLogger(__name__)


class PurchaseSuggestionGenerate(models.TransientModel):
    _name = 'purchase.suggest.generate'
    _description = 'Start to generate the purchase suggestions'

    categ_id = fields.Many2one(
        'product.category', string='Product Category')
    seller_id = fields.Many2one(
        'res.partner', string='Supplier',
        domain=[('supplier', '=', True), ('is_company', '=', True)])
    location_id = fields.Many2one(
        'stock.location', string='Stock Location', required=True,
        default=lambda self: self.env.ref('stock.stock_location_stock'))

    @api.model
    def _prepare_suggest_line(self, product_id, qty_dict):
        porderline_id = False
        if qty_dict['product'].seller_id:
            porderlines = self.env['purchase.order.line'].search([
                ('state', 'not in', ('draft', 'cancel')),
                ('product_id', '=', product_id)],
                order='id desc', limit=1)
            # I cannot filter on 'date_order' because it is not a stored field
            porderline_id = porderlines and porderlines[0].id or False
        sline = {
            'product_id': product_id,
            'seller_id': qty_dict['product'].seller_id.id or False,
            'qty_available': qty_dict['qty_available'],
            'incoming_qty': qty_dict['incoming_qty'],
            'outgoing_qty': qty_dict['outgoing_qty'],
            'draft_po_qty': qty_dict['draft_po_qty'],
            'orderpoint_id': qty_dict['orderpoint'].id,
            'min_qty': qty_dict['min_qty'],
            'last_po_line_id': porderline_id,
            }
        return sline

    @api.multi
    def run(self):
        self.ensure_one()
        pso = self.env['purchase.suggest']
        polo = self.env['purchase.order.line']
        swoo = self.env['stock.warehouse.orderpoint']
        ppo = self.env['product.product']
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
            products_subset = ppo.search(product_domain)
            op_domain.append(('product_id', 'in', products_subset.ids))
        ops = swoo.search(op_domain)
        p_suggest_lines = []
        products = {}
        # key = product_id
        # value = {'virtual_qty': 1.0, 'draft_po_qty': 4.0, 'min_qty': 6.0}
        # TODO : handle the uom
        logger.info('Starting to compute the purchase suggestions')
        for op in ops:
            if op.product_id.id not in products:
                products[op.product_id.id] = {
                    'min_qty': op.product_min_qty,
                    'draft_po_qty': 0.0,
                    'orderpoint': op,
                    'product': op.product_id
                    }
            else:
                raise Warning(
                    _("There are 2 orderpoints (%s and %s) for the same "
                        "product on stock location %s or its "
                        "children.") % (
                        products[op.product_id.id]['orderpoint'].name,
                        op.name,
                        self.location_id.complete_name))
        logger.info('Min qty computed on %d products', len(products))
        polines = polo.search([
            ('state', '=', 'draft'), ('product_id', 'in', products.keys())])
        for line in polines:
            products[line.product_id.id]['draft_po_qty'] += line.product_qty
        logger.info('Draft PO qty computed on %d products', len(products))
        virtual_qties = self.pool['product.product']._product_available(
            self._cr, self._uid, products.keys(),
            context={'location': self.location_id.id})
        logger.info('Stock levels qty computed on %d products', len(products))
        for product_id, qty_dict in products.iteritems():
            qty_dict['virtual_available'] =\
                virtual_qties[product_id]['virtual_available']
            qty_dict['incoming_qty'] =\
                virtual_qties[product_id]['incoming_qty']
            qty_dict['outgoing_qty'] =\
                virtual_qties[product_id]['outgoing_qty']
            qty_dict['qty_available'] =\
                virtual_qties[product_id]['qty_available']
            logger.debug(
                'Product ID: %d Virtual qty = %s Draft PO qty = %s '
                'Min. qty = %s',
                product_id, qty_dict['virtual_available'],
                qty_dict['draft_po_qty'], qty_dict['min_qty'])
            if float_compare(
                    qty_dict['virtual_available'] + qty_dict['draft_po_qty'],
                    qty_dict['min_qty'],
                    precision_rounding=op.product_uom.rounding) < 0:
                vals = self._prepare_suggest_line(product_id, qty_dict)
                if vals:
                    p_suggest_lines.append(vals)
                    logger.debug(
                        'Created a procurement suggestion for product ID %d',
                        product_id)
        p_suggest_lines_sorted = sorted(
            p_suggest_lines, key=lambda to_sort: to_sort['seller_id'])
        if p_suggest_lines_sorted:
            p_suggest_ids = []
            for p_suggest_line in p_suggest_lines_sorted:
                p_suggest = pso.create(p_suggest_line)
                p_suggest_ids.append(p_suggest.id)
            action = self.env['ir.actions.act_window'].for_xml_id(
                'purchase_suggest', 'purchase_suggest_action')
            action.update({
                'target': 'current',
                'domain': [('id', 'in', p_suggest_ids)],
            })
            return action
        else:
            raise Warning(_(
                "The virtual stock for all related products is above the "
                "minimum stock level."))


class PurchaseSuggest(models.TransientModel):
    _name = 'purchase.suggest'
    _description = 'Purchase Suggestions'
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
    draft_po_qty = fields.Float(
        string='Draft PO Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    last_po_line_id = fields.Many2one(
        'purchase.order.line', string='Last Purchase Order Line',
        readonly=True)
    last_po_date = fields.Datetime(
        related='last_po_line_id.order_id.date_order',
        string='Date of the Last Order', readonly=True)
    last_po_qty = fields.Float(
        related='last_po_line_id.product_qty', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        string='Quantity of the Last Order')
    orderpoint_id = fields.Many2one(
        'stock.warehouse.orderpoint', string='Re-ordering Rule',
        readonly=True)
    min_qty = fields.Float(
        string="Min Quantity", readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    qty_to_order = fields.Float(
        string='Quantity to Order',
        digits=dp.get_precision('Product Unit of Measure'))


class PurchaseSuggestPoCreate(models.TransientModel):
    _name = 'purchase.suggest.po.create'
    _description = 'PurchaseSuggestPoCreate'

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
        for line in self.env['purchase.suggest'].browse(psuggest_ids):
            if not line.qty_to_order:
                continue
            if not line.product_id.seller_id:
                raise Warning(_(
                    "No supplier configured for product '%s'.")
                    % line.product_id.name)
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
