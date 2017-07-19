# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class StockChangeProductQty(models.TransientModel):
    _inherit = 'stock.change.product.qty'

    @api.model
    def default_get(self, fields_list):
        res = super(StockChangeProductQty, self).default_get(fields_list)
        if self.env.user.context_default_warehouse_id:
            res['location_id'] = self.env.user.context_default_warehouse_id.\
                lot_stock_id.id
        return res
