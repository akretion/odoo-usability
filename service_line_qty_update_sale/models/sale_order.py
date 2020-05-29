# Copyright 2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_service = fields.Boolean(compute='_compute_has_service')

    @api.depends('order_line.product_id.type')
    def _compute_has_service(self):
        for order in self:
            has_service = False
            for l in order.order_line:
                if l.product_id.type == 'service':
                    has_service = True
                    break
            order.has_service = has_service
