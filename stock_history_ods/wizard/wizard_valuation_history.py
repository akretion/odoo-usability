# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockValuationHistory(models.TransientModel):
    _inherit = 'wizard.valuation.history'

    def report_py3o(self):
        ppo = self.env['product.product']
        lines = self.env['stock.history'].with_context(
            history_date=self.date).read_group(
                [('date', '<=', self.date)],
                ['product_id', 'location_id', 'move_id', 'company_id',
                 'date', 'quantity', 'inventory_value'],
                ['product_id', 'location_id'])
        categ_id2name = {}
        for categ in self.env['product.category'].search([]):
            categ_id2name[categ.id] = categ.display_name
        res = []
        for line in lines:
            product_id = line['product_id'][0]
            product = ppo.browse(product_id)
            res.append({
                'product_categ': categ_id2name[product.categ_id.id],
                'product_name': product.name,
                'product_code': product.default_code,
                'product_display_name': line['product_id'][1],
                'product_uom': product.uom_id.name,
                'quantity': line['quantity'],
                'inventory_value': line['inventory_value'],
            })
        return res

    def print_table(self):
        self.ensure_one()
        action = self.env['report'].get_action(self, 'stock.history.ods')
        return action
