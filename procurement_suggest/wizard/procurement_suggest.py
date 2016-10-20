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
from openerp.tools import float_compare
import logging

logger = logging.getLogger(__name__)


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
        # TODO This code must be fixed in case of multicompany project

    @api.model
    def _compute_procurement_qty(self, orderpoint):
        procs = self.env['procurement.order'].search([
            ('state', 'not in', ('cancel', 'done', 'exception')),
            ('orderpoint_id', '=', orderpoint.id)])
        puo = self.env['product.uom']
        proc_qty = 0
        for proc in procs:
            proc_qty += puo._compute_qty_obj(
                proc.product_uom, proc.product_qty, proc.product_id.uom_id)
            # Only take into account the qty that is not already
            # in the incoming qty or qty on hand
            for move in proc.move_ids:
                if move.state == 'draft':
                    proc_qty -= move.product_qty
        return proc_qty

    @api.model
    def _prepare_suggest_line(self, orderpoint):
        sline = {
            'product_id': orderpoint.product_id.id,
            'seller_id': orderpoint.product_id.seller_id.id or False,
            'qty_available': orderpoint.product_id.qty_available,
            'incoming_qty': orderpoint.product_id.incoming_qty,
            'outgoing_qty': orderpoint.product_id.outgoing_qty,
            'procurement_qty': self._compute_procurement_qty(orderpoint),
            'orderpoint_id': orderpoint.id,
            }
        return sline

    @api.multi
    def run(self):
        pso = self.env['procurement.suggest']
        poo = self.env['procurement.order']
        swoo = self.env['stock.warehouse.orderpoint']
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
        ops = swoo.search(op_domain)
        p_suggest_lines = []
        lines = {}  # key = product_id ; value = {'min_qty', ...}
        for op in ops:
            if op.product_id.id in lines:
                raise Warning(
                    _("There are 2 orderpoints (%s and %s) for the same "
                        "product on stock location %s or its "
                        "children.") % (
                        lines[op.product_id.id]['orderpoint'].name,
                        op.name,
                        self.location_id.complete_name))

            virtual_qty = poo._product_virtual_get(op)
            proc_qty = self._compute_procurement_qty(op)
            product_qty = virtual_qty + proc_qty
            logger.debug(
                'Product: %s Virtual qty = %s Cur. proc. qty = %s '
                'Min. qty = %s',
                op.product_id.name, virtual_qty, proc_qty, op.product_min_qty)
            if float_compare(
                    product_qty, op.product_min_qty,
                    precision_rounding=op.product_uom.rounding) < 0:
                logger.debug(
                    'Create a procurement suggestion for %s',
                    op.product_id.name)
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
    procurement_qty = fields.Float(
        string='Current Procurement Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    outgoing_qty = fields.Float(
        string='Outgoing Quantity', readonly=True,
        digits=dp.get_precision('Product Unit of Measure'))
    orderpoint_id = fields.Many2one(
        'stock.warehouse.orderpoint', string='Re-ordering Rule',
        readonly=True)
    uom_id = fields.Many2one(
        'product.uom', related='product_id.uom_id', readonly=True)
    # on orderpoids, uom_id is a related field of product_id.uom_id
    # so I do the same here
    min_qty = fields.Float(
        string="Min Quantity", readonly=True,
        related='orderpoint_id.product_min_qty',
        digits=dp.get_precision('Product Unit of Measure'))
    new_procurement_qty = fields.Float(
        string='New Procurement Quantity',
        digits=dp.get_precision('Product Unit of Measure'))


class ProcurementCreateFromSuggest(models.TransientModel):
    _name = 'procurement.create.from.suggest'
    _description = 'Create Procurements from Procurement Suggestions'

    @api.multi
    def create_proc(self):
        self.ensure_one()
        psuggest_ids = self.env.context.get('active_ids')
        poo = self.env['procurement.order']
        new_procs = poo.browse(False)
        for line in self.env['procurement.suggest'].browse(psuggest_ids):
            if line.new_procurement_qty:
                vals = poo._prepare_orderpoint_procurement(
                    line.orderpoint_id, line.new_procurement_qty)
                vals['origin'] += _(' Suggest')
                vals['name'] += _(' Suggest')
                new_procs += poo.create(vals)
        if new_procs:
            new_procs.signal_workflow('button_confirm')
            new_procs.run()
        else:
            raise Warning(_('All requested quantities are null.'))
        action = self.env['ir.actions.act_window'].for_xml_id(
            'procurement', 'procurement_action')
        action['domain'] = [('id', 'in', new_procs.ids)]
        return action
