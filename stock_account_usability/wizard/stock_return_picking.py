# Copyright 2019 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class StockReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    # Set to_refund to True by default
    @api.model
    def default_get(self, fields_list):
        res = super(StockReturnPicking, self).default_get(fields_list)
        if isinstance(res.get('product_return_moves'), list):
            for l in res['product_return_moves']:
                if len(l) == 3 and isinstance(l[2], dict):
                    l[2]['to_refund'] = True
        return res
