# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    lunch_voucher_product_id = fields.Many2one(
        'product.product', string='Lunch Voucher Product',
        ondelete='restrict')
    lunch_voucher_employer_price = fields.Monetary(
        'Lunch Voucher Employer Price', currency_field='currency_id')

    # Add constrain to check that lunch_voucher_employer_price is between
    # 50% and 60% of the price of lunch_voucher_product_id for France
