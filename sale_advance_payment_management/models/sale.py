# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_line_ids = fields.One2many(
        'account.move.line', 'sale_id', string='Advance Payments',
        readonly=True)
    # residual
