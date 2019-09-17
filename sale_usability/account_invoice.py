# Copyright (C) 2015-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from collections import OrderedDict


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # sale_ids is kind of the symetric field of invoice_ids on sale.order
    sale_ids = fields.Many2many(
        'sale.order', string='Sale Orders', compute="_compute_sale_ids",
        readonly=True, copy=False)
    sale_count = fields.Integer(
        string='Sale Order Count', compute='_compute_sale_ids', readonly=True)

    @api.depends('invoice_line_ids.sale_line_ids')
    def _compute_sale_ids(self):
        for invoice in self:
            if invoice.type == 'out_invoice':
                sales = invoice.invoice_line_ids.mapped('sale_line_ids').\
                    mapped('order_id')
                invoice.sale_ids = sales.ids
                invoice.sale_count = len(sales.ids)
            else:
                invoice.sale_ids = []
                invoice.sale_count = 0

    def show_sale_orders(self):
        self.ensure_one()
        action = self.env.ref('sale.action_orders').read()[0]
        sales = self.sale_ids
        if len(sales) > 1:
            action['domain'] = [('id', 'in', sales.ids)]
        else:
            action.update({
                'res_id': sales.id,
                'view_mode': 'form,tree,kanban,calendar,pivot,graph,activity',
                'views': False,
                })
        return action

    def py3o_lines_layout_groupby_order(self, subtotal=True):
        # This method is an alternative to the method py3o_lines_layout()
        # defined above: you just have to change the call in the invoice
        # ODT template
        self.ensure_one()
        res1 = OrderedDict()
        # {categ(1): {'lines': [l1, l2], 'subtotal': 23.32}}
        soo = self.env['sale.order']
        for line in self.invoice_line_ids:
            order = line.sale_line_ids and line.sale_line_ids[0].order_id\
                or soo
            if order in res1:
                res1[order]['lines'].append(line)
                res1[order]['subtotal'] += line.price_subtotal
            else:
                res1[order] = {
                    'lines': [line],
                    'subtotal': line.price_subtotal}
        # from pprint import pprint
        # pprint(res1)
        res2 = []
        if len(res1) == 1 and not list(res1)[0]:
            # No order at all
            for line in list(res1.values())[0]['lines']:
                res2.append({'line': line})
        else:
            for order, ldict in res1.items():
                res2.append({'categ': order})
                for line in ldict['lines']:
                    res2.append({'line': line})
                if subtotal:
                    res2.append({'subtotal': ldict['subtotal']})
        # res2:
        # [
        #    {'categ': categ(1)},
        #    {'line': invoice_line(2)},
        #    {'line': invoice_line(3)},
        #    {'subtotal': 8932.23},
        # ]
        # pprint(res2)
        return res2
