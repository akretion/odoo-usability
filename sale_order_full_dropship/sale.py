# -*- coding: utf-8 -*-
# Copyright 2018 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    dropship = fields.Boolean(
        string='Dropship', readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        help="If enabled, all the order lines will be set with the "
        "'Drop Shipping' route upon confirmation of the order.")

    def action_confirm(self):
        try:
            ds_route = self.env.ref('stock_dropshipping.route_drop_shipping')
        except ValueError:
            raise UserError(_("Drop shipping route not found."))
        for order in self:
            if order.dropship:
                # no need to exclude service lines
                # by default, the don't generate a procurement
                order.order_line.write({'route_id': ds_route.id})
        return super(SaleOrder, self).action_confirm()
