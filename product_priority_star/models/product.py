# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _order = "priority desc, name, id"

    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Top List'),
        ], default='0', index=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _order = 'priority desc, default_code, name, id'
