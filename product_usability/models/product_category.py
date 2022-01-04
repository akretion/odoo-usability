# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = ['product.category', "mail.thread", "mail.activity.mixin"]
    _name = 'product.category'

    name = fields.Char(tracking=10)
    parent_id = fields.Many2one(tracking=20)
