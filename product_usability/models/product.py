# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(
        track_visibility='onchange',
        copy=False)

    barcode = fields.Char(
        track_visibility='onchange',
        copy=False)

    weight = fields.Float(
        track_visibility='onchange')

    active = fields.Boolean(
        track_visibility='onchange')

    price_history_ids = fields.One2many(
        comodel_name='product.price.history',
        inverse_name='product_id',
        string='Product Price History')

    _sql_constraints = [(
        # Maybe it could be better to have a constrain per company
        # but the company_id field is on product.template,
        # not on product.product
        # If it's a problem, we'll create a company_id field on
        # product.product
        'default_code_uniq',
        'unique(default_code)',
        'This internal reference already exists!')]

    def show_product_price_history(self):
        self.ensure_one()
        action = self.env.ref(
            'product_usability.product_price_history_action').read()[0]
        action['domain'] = [('product_id', '=', self.id)]
        return action
