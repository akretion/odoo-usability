# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductPriceHistory(models.Model):
    _inherit = 'product.price.history'

    company_currency_id = fields.Many2one(
        related='company_id.currency_id',
        readonly=True,
        compute_sudo=True,
        string='Company Currency')
