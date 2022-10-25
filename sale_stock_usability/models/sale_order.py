# Copyright 2015-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare, float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(tracking=True)
    incoterm = fields.Many2one(tracking=True)

    def report_qty_to_deliver(self):
        # Can be useful for delivery report
        self.ensure_one()
        res = []
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for line in self.order_line:
            if (
                    line.product_id.type in ('product', 'consu') and
                    float_compare(
                        line.product_uom_qty, line.qty_delivered,
                        precision_digits=prec) > 0):
                qty_to_deliver = float_round(
                    line.product_uom_qty - line.qty_delivered, precision_digits=prec)
                res.append({
                    'product': line.product_id,
                    'name': line.name,
                    'uom': line.product_uom,
                    'qty_to_deliver': qty_to_deliver,
                    })
        return res
