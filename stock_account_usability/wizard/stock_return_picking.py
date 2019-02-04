# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class StockReturnPickingLine(models.TransientModel):
    _inherit = 'stock.return.picking.line'

    to_refund = fields.Boolean(default=True)
