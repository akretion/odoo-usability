# -*- coding: utf-8 -*-
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api
from odoo.tools import float_is_zero
from itertools import groupby


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(track_visibility='onchange')
    date_confirm = fields.Date(track_visibility='onchange')
    client_order_ref = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
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
        res1 = []
        # [
        #    {'categ': categ(6), 'lines': [l1, l2], 'subtotal': 23.32},
        #    {'categ': categ(1), 'lines': [l3, l4, l5], 'subtotal': 12.42},
        # ]
        for categ, lines in groupby(self.order_line, lambda l: l.layout_category_id):
            entry = {'lines': [], 'categ': categ}
            if categ.subtotal:
                entry['subtotal'] = 0.0
            for line in lines:
                entry['lines'].append(line)
                if 'subtotal' in entry:
                    entry['subtotal'] += line.price_subtotal
            res1.append(entry)
        res2 = []
        if len(res1) == 1 and not res1[0]['categ']:
            # No category at all
            for l in res1[0]['lines']:
                res2.append({'line': l})
        else:
            # TODO : gérer qd il n'y a pas de categ
            for ldict in res1:
                res2.append({'categ': ldict['categ']})
                for soline in ldict['lines']:
                    res2.append({'line': soline})
                if 'subtotal' in ldict:
                    res2.append({'subtotal': ldict['subtotal']})
        # res2:
        # [
        #    {'categ': categ(1)},
        #    {'line': sale_order_line(2)},
        #    {'line': sale_order_line(3)},
        #    {'subtotal': 8932.23},
        # ]
        return res2

class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    sale_ids = fields.One2many(
        'sale.order', 'procurement_group_id', string='Sale Orders',
        readonly=True)
