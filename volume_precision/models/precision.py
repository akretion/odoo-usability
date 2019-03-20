# Copyright 2019 David BEAL @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    volume = fields.Float(digits=dp.get_precision('Volume'))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    volume = fields.Float(digits=dp.get_precision('Volume'))


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float(digits=dp.get_precision('Volume'))
