# Copyright 2019-2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    commission_product_id = fields.Many2one(
        related='company_id.commission_product_id', readonly=False)
    commission_po_config = fields.Selection(related="company_id.commission_po_config", readonly=False)
