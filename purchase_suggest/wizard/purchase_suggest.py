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
from openerp.tools import float_compare, float_is_zero
from openerp.exceptions import Warning
import logging

logger = logging.getLogger(__name__)


class PurchaseSuggestGenerate(models.TransientModel):
    _name = 'purchase.suggest.generate'
    _description = 'Start to generate the purchase suggestions'

    categ_ids = fields.Many2many(
        'product.category', string='Product Categories')
    seller_ids = fields.Many2many(
        'res.partner', string='Suppliers',
        domain=[('supplier', '=', True)])
    location_id = fields.Many2one(
        'stock.location', string='Stock Location', required=True,
        default=lambda self: self.env.ref('stock.stock_location_stock'))

    @api.model
    def _prepare_suggest_line(self, product_id, qty_dict):
        porderline_id = False
        porderlines = self.env['purchase.order.line'].search([
            ('state', 'not in', ('draft', 'cancel')),
            ('product_id', '=', product_id)],
            order='id desc', limit=1)
        # I cannot filter on 'date_order' because it is not a stored field
        porderline_id = porderlines and porderlines[0].id or False
        future_qty = qty_dict['virtual_available'] + qty_dict['draft_po_qty']
        if float_compare(
                qty_dict['max_qty'], qty_dict['min_qty'],
                precision_rounding=qty_dict['product'].uom_id.rounding) == 1:
            # order to go up to qty_max
            qty_to_order = qty_dict['max_qty'] - future_qty
        else:
            # order to go up to qty_min
            qty_to_order = qty_dict['min_qty'] - future_qty

        sline = {
            'company_id':
            qty_dict['orderpoint'] and qty_dict['orderpoint'].company_id.id,
            'product_id': product_id,
            'seller_id': qty_dict['product'].seller_id.id or False,
            'qty_available': qty_dict['qty_available'],
            'incoming_qty': qty_dict['incoming_qty'],
            'outgoing_qty': qty_dict['outgoing_qty'],
            'draft_po_qty': qty_dict['draft_po_qty'],
            'orderpoint_id':
            qty_dict['orderpoint'] and qty_dict['orderpoint'].id,
            'location_id': self.location_id.id,
            'min_qty': qty_dict['min_qty'],
            'max_qty': qty_dict['max_qty'],
            'last_po_line_id': porderline_id,
            'qty_to_order': qty_to_order,
            }
        return sline

    @api.model
    def _prepare_product_domain(self):
        product_domain = []
        if self.categ_ids:
            product_domain.append(
                ('categ_id', 'child_of', self.categ_ids.ids))
        if self.seller_ids:
            product_domain.append(
                ('seller_id', 'in', self.seller_ids.ids))
        return product_domain

    @api.model
    def generate_products_dict(self):
        ppo = self.env['product.product']
        swoo = self.env['stock.warehouse.orderpoint']
        products = {}
        op_domain = [
            ('suggest', '=', True),
            ('company_id', '=', self.env.user.company_id.id),
            ('location_id', 'child_of', self.location_id.id),
            ]
        if self.categ_ids or self.seller_ids:

            products_subset = ppo.search(self._prepare_product_domain())
            op_domain.append(('product_id', 'in', products_subset.ids))
        ops = swoo.search(op_domain)
        for op in ops:
            if op.product_id.id not in products:
                products[op.product_id.id] = {
                    'min_qty': op.product_min_qty,
                    'max_qty': op.product_max_qty,
                    'draft_po_qty': 0.0,  # This value is set later on
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
        return products

    @api.multi
    def run(self):
        self.ensure_one()
        pso = self.env['purchase.suggest']
        polo = self.env['purchase.order.line']
        puo = self.env['product.uom']
        p_suggest_lines = []
        products = self.generate_products_dict()
        # key = product_id
        # value = {'virtual_qty': 1.0, 'draft_po_qty': 4.0, 'min_qty': 6.0}
        # WARNING: draft_po_qty is in the UoM of the product
        logger.info('Starting to compute the purchase suggestions')
        logger.info('Min qty computed on %d products', len(products))
        polines = polo.search([
            ('state', '=', 'draft'), ('product_id', 'in', products.keys())])
        for line in polines:
            qty_product_po_uom = puo._compute_qty_obj(
                line.product_uom, line.product_qty, line.product_id.uom_id)
            products[line.product_id.id]['draft_po_qty'] += qty_product_po_uom
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
            compare = float_compare(
                qty_dict['virtual_available'] + qty_dict['draft_po_qty'],
                qty_dict['min_qty'],
                precision_rounding=qty_dict['product'].uom_id.rounding)
            if compare < 0:
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
                "There are no purchase suggestions to generate."))


class PurchaseSuggest(models.TransientModel):
    _name = 'purchase.suggest'
    _description = 'Purchase Suggestions'
    _rec_name = 'product_id'

    company_id = fields.Many2one(
        'res.company', string='Company', required=True)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True, readonly=True)
    uom_id = fields.Many2one(
        'product.uom', string='UoM', related='product_id.uom_id',
        readonly=True)
    uom_po_id = fields.Many2one(
        'product.uom', string='Purchase UoM', related='product_id.uom_po_id',
        readonly=True)
    seller_id = fields.Many2one(
        'res.partner', string='Supplier', readonly=True,
        domain=[('supplier', '=', True)])
    qty_available = fields.Float(
        string='Quantity On Hand', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="in the unit of measure of the product")
    incoming_qty = fields.Float(
        string='Incoming Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="in the unit of measure of the product")
    outgoing_qty = fields.Float(
        string='Outgoing Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="in the unit of measure of the product")
    draft_po_qty = fields.Float(
        string='Draft PO Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="Draft purchase order quantity in the unit of measure "
        "of the product (NOT in the purchase unit of measure !)")
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
    last_po_uom = fields.Many2one(
        related='last_po_line_id.product_uom', readonly=True,
        string='UoM of the Last Order')
    orderpoint_id = fields.Many2one(
        'stock.warehouse.orderpoint', string='Re-ordering Rule',
        readonly=True)
    location_id = fields.Many2one(
        'stock.location', string='Stock Location', readonly=True)
    min_qty = fields.Float(
        string="Min Quantity", readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="in the unit of measure for the product")
    max_qty = fields.Float(
        string="Max Quantity", readonly=True,
        digits=dp.get_precision('Product Unit of Measure'),
        help="in the unit of measure for the product")
    qty_to_order = fields.Float(
        string='Quantity to Order',
        digits=dp.get_precision('Product Unit of Measure'),
        help="Quantity to order in the purchase unit of measure for the "
        "product")


class PurchaseSuggestPoCreate(models.TransientModel):
    _name = 'purchase.suggest.po.create'
    _description = 'PurchaseSuggestPoCreate'

    def _prepare_purchase_order(self, partner, company, location):
        poo = self.env['purchase.order']
        spto = self.env['stock.picking.type']
        po_vals = {'partner_id': partner.id, 'company_id': company.id}
        ponull = poo.browse(False)
        partner_change_dict = ponull.onchange_partner_id(partner.id)
        po_vals.update(partner_change_dict['value'])
        pick_type_dom = [
            ('code', '=', 'incoming'),
            ('warehouse_id.company_id', '=', company.id)]
        pick_types = spto.search(
            pick_type_dom + [(
                'default_location_dest_id', 'child_of', location.id)])
        # I use location.parent_id.id to support 2 step-receptions
        # where the stock.location .type is linked to Warehouse > Receipt
        # but location is Warehouse > Stock
        if not pick_types:
            pick_types = spto.search(
                pick_type_dom + [(
                    'default_location_dest_id',
                    'child_of',
                    location.location_id.id)])
        if not pick_types:
            pick_types = spto.search(pick_type_dom)
            if not pick_types:
                raise Warning(_(
                    "Make sure you have at least an incoming picking "
                    "type defined"))
        po_vals['picking_type_id'] = pick_types[0].id
        pick_type_dict = ponull.onchange_picking_type_id(pick_types[0].id)
        po_vals.update(pick_type_dict['value'])
        return po_vals

    def _prepare_purchase_order_line(
            self, partner, product, qty_to_order, uom):
        polo = self.env['purchase.order.line']
        polnull = polo.browse(False)
        product_change_res = polnull.onchange_product_id(
            partner.property_product_pricelist_purchase.id,
            product.id, qty_to_order, uom.id, partner.id,
            fiscal_position_id=partner.property_account_position.id)
        product_change_vals = product_change_res['value']
        taxes_id_vals = []
        if product_change_vals.get('taxes_id'):
            for tax_id in product_change_vals['taxes_id']:
                taxes_id_vals.append((4, tax_id))
            product_change_vals['taxes_id'] = taxes_id_vals
        vals = dict(product_change_vals, product_id=product.id)
        return vals

    def _create_update_purchase_order(
            self, partner, company, po_lines, location):
        polo = self.env['purchase.order.line']
        poo = self.env['purchase.order']
        puo = self.env['product.uom']
        existing_pos = poo.search([
            ('partner_id', '=', partner.id),
            ('company_id', '=', company.id),
            ('state', '=', 'draft'),
            ('location_id', '=', location.id),
            ])
        if existing_pos:
            # update the first existing PO
            existing_po = existing_pos[0]
            for product, qty_to_order, uom in po_lines:
                existing_polines = polo.search([
                    ('product_id', '=', product.id),
                    ('order_id', '=', existing_po.id),
                    ])
                if existing_polines:
                    existing_poline = existing_polines[0]
                    existing_poline.product_qty += puo._compute_qty_obj(
                        uom, qty_to_order, existing_poline.product_uom)
                else:
                    pol_vals = self._prepare_purchase_order_line(
                        partner, product, qty_to_order, uom)
                    pol_vals['order_id'] = existing_po.id
                    polo.create(pol_vals)
            existing_po.message_post(
                _('Purchase order updated from purchase suggestions.'))
            return existing_po
        else:
            # create new PO
            po_vals = self._prepare_purchase_order(partner, company, location)
            order_lines = []
            for product, qty_to_order, uom in po_lines:
                pol_vals = self._prepare_purchase_order_line(
                    partner, product, qty_to_order, uom)
                order_lines.append((0, 0, pol_vals))
            po_vals['order_line'] = order_lines
            new_po = poo.create(po_vals)
            return new_po

    @api.multi
    def create_po(self):
        self.ensure_one()
        # group by supplier
        po_to_create = {}
        # key = (seller, company)
        # value = [(product1, qty1, uom1), (product2, qty2, uom2)]
        psuggest_ids = self.env.context.get('active_ids')
        location = False
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self.env['purchase.suggest'].browse(psuggest_ids):
            if not location:
                location = line.location_id
            if float_is_zero(line.qty_to_order, precision_digits=precision):
                continue
            if not line.product_id.seller_id:
                raise Warning(_(
                    "No supplier configured for product '%s'.")
                    % line.product_id.name)
            po_to_create.setdefault(
                (line.seller_id, line.company_id), []).append(
                (line.product_id, line.qty_to_order, line.uom_po_id))
        if not po_to_create:
            raise Warning(_('No purchase orders created or updated'))
        po_ids = []
        for (seller, company), po_lines in po_to_create.iteritems():
            assert location, 'No stock location'
            po = self._create_update_purchase_order(
                seller, company, po_lines, location)
            po_ids.append(po.id)

        action = self.env['ir.actions.act_window'].for_xml_id(
            'purchase', 'purchase_rfq')
        action['domain'] = [('id', 'in', po_ids)]
        return action
