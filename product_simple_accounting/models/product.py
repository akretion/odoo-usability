# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class ProductProfile(models.Model):
    _inherit = 'product.profile'

    def _get_types(self):
        return [('product', 'Stockable Product'),
                ('consu', 'Consumable'),
                ('service', 'Service')]

    property_account_income = fields.Many2one(
        'account.account',
        'Property Account Income',
        company_dependent=True)
    property_account_expense = fields.Many2one(
        'account.account',
        'Property Account Expense',
        company_dependent=True)
