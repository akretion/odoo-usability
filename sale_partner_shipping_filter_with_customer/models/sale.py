# coding: utf-8
# © 2017 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    parent_id = fields.Many2one(related='partner_id.parent_id',
                                        readonly=True)
