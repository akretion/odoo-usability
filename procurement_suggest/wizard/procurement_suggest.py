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
        sline = {
            'product_id': orderpoint.product_id.id,
            'seller_id': orderpoint.product_id.seller_id.id or False,
            'qty_available': orderpoint.product_id.qty_available,
            'incoming_qty': orderpoint.product_id.incoming_qty,
            'outgoing_qty': orderpoint.product_id.outgoing_qty,
            'orderpoint_id': orderpoint.id,
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
            # TODO : take into account the running procurements ?
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
    procurement_qty = fields.Float(
        string='Procurement Quantity',
        digits=dp.get_precision('Product Unit of Measure'))


class ProcurementCreateFromSuggest(models.TransientModel):
    _name = 'procurement.create.from.suggest'
    _description = 'Create Procurements from Procurement Suggestions'

    @api.model
    def _prepare_procurement_order(self, proc_suggest):
        proc_vals = {
            'name': u'INT: ' + unicode(self.env.user.login),
            'product_id': proc_suggest.product_id.id,
            'product_qty': proc_suggest.procurement_qty,
            'product_uom': proc_suggest.uom_id.id,
            'location_id': proc_suggest.orderpoint_id.location_id.id,
            'company_id': proc_suggest.orderpoint_id.company_id.id,
            'origin': _('Procurement Suggest'),
            }
        return proc_vals

    @api.multi
    def create_proc(self):
        self.ensure_one()
        psuggest_ids = self.env.context.get('active_ids')
        poo = self.env['procurement.order']
        new_procs = poo.browse(False)
        for line in self.env['procurement.suggest'].browse(psuggest_ids):
            if line.procurement_qty:
                vals = self._prepare_procurement_order(line)
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
