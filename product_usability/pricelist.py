# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    company_id = fields.Many2one(
        default=lambda self: self.env['res.company']._company_default_get())
