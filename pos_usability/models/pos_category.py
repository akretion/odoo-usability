# Copyright 2017-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PosCategory(models.Model):
    _inherit = 'pos.category'

    product_count = fields.Integer(
        '# Products', compute='_compute_product_count',
        help="The number of products under this point of sale category "
        "(children categories included)")

    # inspired by the code of odoo/addons/product/models/product_category.py
    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group(
            [('pos_categ_id', 'child_of', self.ids)],
            ['pos_categ_id'], ['pos_categ_id'])
        group_data = dict(
            (data['pos_categ_id'][0], data['pos_categ_id_count']) for data
            in read_group_res)
        for pos_categ in self:
            product_count = 0
            for sub_categ_id in pos_categ.search([('id', 'child_of', pos_categ.ids)]).ids:
                product_count += group_data.get(sub_categ_id, 0)
            pos_categ.product_count = product_count
