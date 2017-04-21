# coding: utf-8
# © 2017 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commercial_partner_id = fields.Many2one(
        related='partner_id.commercial_partner_id', readonly=True)
