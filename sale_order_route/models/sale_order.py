# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    route_id = fields.Many2one(
        'stock.location.route', string='Route',
        ondelete='restrict', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain=[('sale_selectable', '=', True)])

    def _action_confirm(self):
        for order in self.filtered(lambda o: o.route_id):
            order.order_line.filtered(
                lambda l: l.product_id.type in ('product', 'consu')).write(
                    {'route_id': order.route_id.id})
        super(SaleOrder, self)._action_confirm()
