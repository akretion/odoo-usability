# Copyright 2017-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PosCategory(models.Model):
    _inherit = 'pos.category'

    product_count = fields.Integer(
        '# Products', compute='_compute_product_count',
        help="The number of products under this point of sale category "
        "(does not consider the children categories)")

    # inspired by the code of odoo/addons/product/models/product.py
    def _compute_product_count(self):
        read_group_res = self.env['product.template'].read_group(
            [('pos_categ_id', 'in', self.ids)],
            ['pos_categ_id'], ['pos_categ_id'])
        group_data = dict(
            (data['pos_categ_id'][0], data['pos_categ_id_count']) for data
            in read_group_res)
        for pos_categ in self:
            pos_categ.product_count = group_data.get(pos_categ.id, 0)
