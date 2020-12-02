# Copyright 2014-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_stock_move_lines_reserved(self):
        self.ensure_one()
        action = self.action_view_stock_moves()
        action['context'] = {'search_default_todo': True}
        return action
