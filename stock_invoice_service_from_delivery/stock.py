# -*- coding: utf-8 -*-
##############################################################################
#
#    Stock Invoice Service from Delivery module for OpenERP
#    Copyright (C) 2013 Akretion (http://www.akretion.com)
#    Copyright (C) 2004-2010 OpenERP S.A.
#    @author: Alexis de Lattre <alexis.delattre@akretion.com>
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

from openerp.osv import orm


class stock_picking(orm.Model):
    _inherit = 'stock.picking'

    # Fixes this bug : https://bugs.launchpad.net/openobject-addons/+bug/1167330
    # [Trunk/7.0] Service article not invoiced by invoice on delivery
    # This code has been taken from addons-6.1/sale/stock.py line 124
    # and only received minor modifications
    def action_invoice_create(self, cr, uid, ids, journal_id=False,
        group=False, type='out_invoice', context=None):
        if context is None:
            context = {}
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        picking_obj = self.pool.get('stock.picking')
        order_line_obj = self.pool.get('sale.order.line')

        result = super(stock_picking, self).action_invoice_create(cr, uid,
            ids, journal_id=journal_id, group=group, type=type,
            context=context)
        picking_ids = result.keys()
        invoice_ids = result.values()
        invoices = {}
        for invoice in invoice_obj.browse(cr, uid, invoice_ids,
                context=context):
            invoices[invoice.id] = invoice

        for picking in picking_obj.browse(cr, uid, picking_ids,
            context=context):
            if not picking.sale_id or picking.backorder_id:
                continue

            for sale_line in picking.sale_id.order_line:
                sale_line_invoiced = order_line_obj.read(cr, uid, sale_line.id, ['invoiced'], context=context)['invoiced']
                # If I use a browse to get the 'invoiced' field of the sale order
                # line, then, if I het the following bug :
                # If I select 2 pickings linked to the same sale order,
                # and I create an invoice with "group by partner = True",
                # then the service line will be generated twice, because
                # sale_line.invoiced = False even after the write {'invoiced': True}
                # at the end of this function
                if sale_line.product_id.type == 'service' and not sale_line_invoiced:
                    if not type:
                        type = context.get('inv_type', False)
                    if group:
                        name = picking.name + '-' + sale_line.name
                    else:
                        name = sale_line.name
                    if type in ('out_invoice', 'out_refund'):
                        account_id = sale_line.product_id.property_account_income.id
                        if not account_id:
                            account_id = sale_line.product_id.categ_id.\
                                    property_account_income_categ.id
                    else:
                        account_id = sale_line.product_id.\
                                property_account_expense.id
                        if not account_id:
                            account_id = sale_line.product_id.categ_id.\
                                    property_account_expense_categ.id

                    vals = order_line_obj._prepare_order_line_invoice_line(cr, uid, sale_line, account_id, context=context)
                    if vals:
                        vals['name'] = name
                        vals['account_analytic_id'] = self._get_account_analytic_invoice(cr, uid, picking, sale_line)
                        vals['invoice_id'] = invoices[result[picking.id]].id
                        invoice_line_id = invoice_line_obj.create(cr, uid, vals, context=context)
                        sale_line.write({
                            'invoiced': True,
                            'invoice_lines': [(6, 0, [invoice_line_id])],
                        }, context=context)
        return result

