# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PurchaseConfigSettings(models.TransientModel):
    _inherit = 'purchase.config.settings'

    lunch_voucher_natixis_customer_code = fields.Char(
        related='company_id.lunch_voucher_natixis_customer_code')
    lunch_voucher_natixis_delivery_code = fields.Char(
        related='company_id.lunch_voucher_natixis_delivery_code')
