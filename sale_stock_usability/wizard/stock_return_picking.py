# Copyright 2017-2019 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    @api.model
    def default_get(self, fields):
        res = super(StockReturnPicking, self).default_get(fields)
        if res.get('product_return_moves'):
            for line in res['product_return_moves']:
                if len(line) == 3:
                    line[2]['to_refund_so'] = True
        return res
