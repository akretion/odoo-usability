# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def set_quantity_zero(self):
        self.ensure_one()
        self.product_return_moves.write({'quantity': 0})
        action = self.env.ref('stock.act_stock_return_picking').read()[0]
        action['res_id'] = self.id
        return action
