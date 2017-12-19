# -*- coding: utf-8 -*-
# © 2017 Akretion - Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'purchase.config.settings'

    lunch_voucher_product_id = fields.Many2one(
        related='company_id.lunch_voucher_product_id')
    lunch_voucher_employer_price = fields.Monetary(
        related='company_id.lunch_voucher_employer_price',
        currency_field='company_currency_id')
