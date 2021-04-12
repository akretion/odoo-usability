# Copyright 2016-2021 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tracking = fields.Selection(tracking=True)
    sale_delay = fields.Float(tracking=True)
    # the 'stock' module adds 'product' in type...
    # but forgets to make it the default
    type = fields.Selection(default='product')

    def action_view_stock_move(self):
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        action['context'] = {'search_default_done': True}
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_view_stock_move(self):
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id', 'in', self.ids)]
        action['context'] = {'search_default_done': True}
        return action
