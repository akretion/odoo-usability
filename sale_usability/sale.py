# Copyright (C) 2015-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.tools import float_is_zero
from collections import OrderedDict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(track_visibility='onchange')
    confirmation_date = fields.Datetime(track_visibility='onchange')
    client_order_ref = fields.Char(track_visibility='onchange')
    # for partner_id, the 'sale' module sets track_visibility='always'
    partner_id = fields.Many2one(track_visibility='onchange')
    amount_tax = fields.Monetary(track_visibility='onchange')
    partner_shipping_id = fields.Many2one(track_visibility='onchange')
    partner_invoice_id = fields.Many2one(track_visibility='onchange')
    pricelist_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    # for reports
    has_discount = fields.Boolean(
        compute='_compute_has_discount', readonly=True)

    @api.multi
    def _compute_has_discount(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        for order in self:
            has_discount = False
            for line in order.order_line:
                if not float_is_zero(line.discount, precision_digits=prec):
                    has_discount = True
                    break
            order.has_discount = has_discount

    # for report
    @api.multi
    def py3o_lines_layout(self):
        self.ensure_one()
        res1 = OrderedDict()
        # {categ(6): {'lines': [l1, l2], 'subtotal': 23.32}}
        for line in self.order_line:
            categ = line.layout_category_id
            if categ in res1:
                res1[categ]['lines'].append(line)
                res1[categ]['subtotal'] += line.price_subtotal
            else:
                res1[categ] = {
                    'lines': [line],
                    'subtotal': line.price_subtotal}

        res2 = []
        if len(res1) == 1 and not res1.keys()[0]:
            # No category at all
            for line in res1.values()[0]['lines']:
                res2.append({'line': line})
        else:
            for categ, ldict in res1.iteritems():
                res2.append({'categ': categ})
                for line in ldict['lines']:
                    res2.append({'line': line})
                if categ.subtotal:
                    res2.append({'subtotal': ldict['subtotal']})
        # res2:
        # [
        #    {'categ': categ(1)},
        #    {'line': sale_order_line(2)},
        #    {'line': sale_order_line(3)},
        #    {'subtotal': 8932.23},
        # ]
        return res2
