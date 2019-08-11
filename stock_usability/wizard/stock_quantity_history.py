# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    location_id = fields.Many2one(
        'stock.location', string='Stock Location',
        domain=[('usage', '=', 'internal')],
        help="If you select a stock location, the inventory report will be "
        "for this stock location and its children locations. If you leave "
        "this field empty, the inventory report will be for all the internal "
        "stock locations.")

    def open_table(self):
        action = super(StockQuantityHistory, self).open_table()
        if self.compute_at_date:
            action['domain'] = "[('type', '=', 'product'), ('qty_available', '!=', 0)]"
        if self.location_id:
            if self.compute_at_date:
                # insert "location" in context for qty computation
                action['context']['location'] = self.location_id.id
            else:
                action['domain'] = [('location_id', 'child_of', self.location_id.id)]
                action['context'] = {}
        return action
