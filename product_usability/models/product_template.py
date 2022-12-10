# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # restore v8 native field
    # https://github.com/odoo/odoo/blob/8.0/addons/product/product.py#L592
    # in v10, that field was defined in procurement_suggest, but we will
    # probably not port procurement_suggest because it is native in v14
    seller_id = fields.Many2one(
        'res.partner', related='seller_ids.partner_id', store=True,
        string='Main Supplier')

    # in v14, I noticed that the tracking of the fields of product.template
    # are only shown in the form view of product.template, not in the form
    # view of product.product
    name = fields.Char(tracking=10)
    barcode = fields.Char(tracking=20)
    default_code = fields.Char(tracking=30)
    categ_id = fields.Many2one(tracking=40)
    detailed_type = fields.Selection(tracking=50)
    list_price = fields.Float(tracking=60, default=0)  # native: default=1.0
    weight = fields.Float(tracking=70)
    sale_ok = fields.Boolean(tracking=80)
    purchase_ok = fields.Boolean(tracking=90)
    active = fields.Boolean(tracking=100)
    company_id = fields.Many2one(tracking=110)
    barcode_type = fields.Char(compute='_compute_template_barcode_type')

    # precompute=True doesn't work on product.template
    # (works fine on product.product), probably because we don't depend
    # on 'barcode'
    @api.depends('product_variant_ids.barcode')
    def _compute_template_barcode_type(self):
        ppo = self.env['product.product']
        for template in self:
            barcode_type = False
            if len(template.product_variant_ids) == 1:
                barcode = template.product_variant_ids.barcode
                barcode_type = ppo._get_barcode_type(barcode)
            template.barcode_type = barcode_type
