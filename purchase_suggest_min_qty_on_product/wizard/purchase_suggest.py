# -*- coding: utf-8 -*-
##############################################################################
#
#    Purchase Suggest Min Qty on Product module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class PurchaseSuggestionGenerate(models.TransientModel):
    _inherit = 'purchase.suggest.generate'

    # Without this module, when we use orderpoints, if there are no orderpoints
    # for a consu product, Odoo will not suggest to re-order it.
    # But, with this module, Odoo will also suggest to re-order the consu
    # products, which may not be what the user wants
    product_type = fields.Selection([
        ('product', 'Stockable Product'),
        ('product_and_consu', 'Consumable and Stockable Product'),
        ], default='product', string='Product Type')

    @api.model
    def _prepare_suggest_line(self, product_id, qty_dict):
        sline = super(PurchaseSuggestionGenerate, self)._prepare_suggest_line(
            product_id, qty_dict)
        sline['company_id'] = self.env.user.company_id.id
        return sline

    @api.model
    def generate_products_dict(self):
        '''inherit the native method to use min_qty/max_qty on
        product.product'''
        ppo = self.env['product.product']
        products = {}
        product_domain = self._prepare_product_domain()
        if self.product_type == 'product':
            product_domain.append(('type', '=', 'product'))
        product_to_analyse = ppo.search(product_domain)
        for product in product_to_analyse:
            # We also want the missing product that have min_qty = 0
            # So we remove "if product.z_stock_min > 0"
            products[product.id] = {
                'min_qty': product.min_qty,
                'max_qty': product.max_qty,
                'draft_po_qty': 0.0,  # This value is set later on
                'orderpoint': False,
                'product': product,
                }
        return products
