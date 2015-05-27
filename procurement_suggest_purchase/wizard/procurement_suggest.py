# -*- encoding: utf-8 -*-
##############################################################################
#
#    Procurement Suggest Purchase module for Odoo
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

from openerp import models, fields, api


class ProcurementSuggestionGenerate(models.TransientModel):
    _inherit = 'procurement.suggest.generate'

    @api.model
    def _prepare_suggest_line(self, orderpoint):
        sline = super(ProcurementSuggestionGenerate, self).\
            _prepare_suggest_line(orderpoint)
        porderline_id = False
        if orderpoint.product_id.seller_id:
            porderlines = self.env['purchase.order.line'].search([
                ('state', 'not in', ('draft', 'cancel')),
                ('product_id', '=', orderpoint.product_id.id)],
                order='id desc', limit=1)
            # I cannot filter on 'date_order' because it is not a stored field
            porderline_id = porderlines and porderlines[0].id or False
        sline['last_po_line_id'] = porderline_id
        return sline


class ProcurementSuggest(models.TransientModel):
    _inherit = 'procurement.suggest'

    last_po_line_id = fields.Many2one(
        'purchase.order.line', string='Last Purchase Order Line',
        readonly=True)
    last_po_date = fields.Datetime(
        related='last_po_line_id.order_id.date_order',
        string='Date of the last PO', readonly=True)
    last_po_qty = fields.Float(
        related='last_po_line_id.product_qty', readonly=True,
        string='Quantity of the Last Order')


class ProcurementCreateFromSuggest(models.TransientModel):
    _inherit = 'procurement.create.from.suggest'

    @api.multi
    def create_proc(self):
        action = super(ProcurementCreateFromSuggest, self).create_proc()
        poo = self.env['procurement.order']
        new_procs = poo.browse(action['domain'][0][2])
        po_ids = []
        for proc in new_procs:
            if proc.purchase_id and proc.purchase_id.id not in po_ids:
                po_ids.append(proc.purchase_id.id)
        if po_ids:
            action = self.env['ir.actions.act_window'].for_xml_id(
                'purchase', 'purchase_rfq')
            action['domain'] = [('id', 'in', po_ids)]
        return action
