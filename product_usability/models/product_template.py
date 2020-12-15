# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # restore v8 native field
    # https://github.com/odoo/odoo/blob/8.0/addons/product/product.py#L592
    # in v10, that field was defined in procurement_suggest, but we will
    # probably not port procurement_suggest because it is native in v14
    seller_id = fields.Many2one(
        'res.partner', related='seller_ids.name', string='Main Supplier')

#    name = fields.Char(
#        track_visibility='onchange')

#    type = fields.Selection(
#        track_visibility='onchange')

#    categ_id = fields.Many2one(
#        track_visibility='onchange')

#    list_price = fields.Float(
#        track_visibility='onchange')

#    sale_ok = fields.Boolean(
#        track_visibility='onchange')

#    purchase_ok = fields.Boolean(
#        track_visibility='onchange')

#    active = fields.Boolean(
#        track_visibility='onchange')
