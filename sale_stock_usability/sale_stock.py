# -*- coding: utf-8 -*-
# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools import float_compare, float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(track_visibility='onchange')
    incoterm = fields.Many2one(track_visibility='onchange')

    def report_qty_to_deliver(self):
        # Can be useful for delivery report
        self.ensure_one()
        res = []
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for l in self.order_line:
            if (
                    l.product_id.type in ('product', 'consu') and
                    float_compare(
                        l.product_uom_qty, l.qty_delivered,
                        precision_digits=prec) > 0):
                qty_to_deliver = float_round(
                    l.product_uom_qty - l.qty_delivered, precision_digits=prec)
                res.append({
                    'product': l.product_id,
                    'name': l.name,
                    'uom': l.product_uom,
                    'qty_to_deliver': qty_to_deliver,
                    })
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def report_qty_to_deliver(self):
        self.ensure_one()
        res = []
        if self.sale_id:
            res = self.sale_id.report_qty_to_deliver()
        return res
