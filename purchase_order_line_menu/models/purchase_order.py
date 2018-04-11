# -*- coding: utf-8 -*-
# Copyright 2018 Raphael Reverdy https://akretion.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    po_name = fields.Char(string="Order", related='order_id.name', store=True)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    pass