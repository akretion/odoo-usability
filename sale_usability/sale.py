# -*- coding: utf-8 -*-
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api
from odoo.tools import float_is_zero
from collections import OrderedDict


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(track_visibility='onchange')
    date_confirm = fields.Date(track_visibility='onchange')
    client_order_ref = fields.Char(track_visibility='onchange')
    # for partner_id, the 'sale' module sets track_visibility='always'
    partner_id = fields.Many2one(track_visibility='onchange')
    # for amount_tax, the 'sale' module sets track_visibility='always'
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

    @api.multi
    def action_confirm(self):
        '''Reload view upon order confirmation to display the 3 qty cols'''
        res = super(SaleOrder, self).action_confirm()
        if len(self) == 1:
            res = self.env['ir.actions.act_window'].for_xml_id(
                'sale', 'action_orders')
            res.update({
                'view_mode': 'form,tree,kanban,calendar,pivot,graph',
                'res_id': self.id,
                'views': False,
                'context': {'hide_sale': False},
                })
        return res

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


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    sale_ids = fields.One2many(
        'sale.order', 'procurement_group_id', string='Sale Orders',
        readonly=True)
