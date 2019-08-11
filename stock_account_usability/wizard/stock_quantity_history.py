# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    def open_table(self):
        action = super(StockQuantityHistory, self).open_table()
        if self.location_id and self.env.context.get('valuation'):
            # When we have 'valuation' in context
            # in both cases ('current inventory' and 'at specific date')
            # it returns an action on product.product,
            # the only difference is the context.
            # We have to make the same modifications, but
            # when self.compute_at_date, action['context'] is a dict
            # otherwize, action['context'] is a string
            if self.compute_at_date:
                # insert "location" in context for qty computation
                action['context']['location'] = self.location_id.id
                # When company_owned=True, the 'location' given in the
                # context is not taken into account
                # IMPORTANT: also requires a patch on the stock_account
                # module. Patch provided in this module.
                action['context']['company_owned'] = False
            else:
                action['context'] = {
                    'location': self.location_id.id,
                    'create': False,
                    'edit': False,
                    }
        return action
