# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'

    order_id = fields.Many2one(
        'sale.order', string='Only for Order', ondelete='cascade')
