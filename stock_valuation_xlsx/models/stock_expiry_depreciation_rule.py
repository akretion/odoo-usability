# Copyright 2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockExpiryDepreciationRule(models.Model):
    _name = 'stock.expiry.depreciation.rule'
    _description = 'Stock Expiry Depreciation Rule'
    _order = 'company_id, start_limit_days'

    company_id = fields.Many2one(
        'res.company', string='Company',
        ondelete='cascade', required=True,
        default=lambda self: self.env.company)
    start_limit_days = fields.Integer(
        string='Days Before/After Expiry', required=True,
        help="Enter negative value for days before expiry. Enter positive values for days after expiry. This value is the START of the time interval when going from future to past.")
    ratio = fields.Integer(string='Depreciation Ratio (%)', required=True)
    name = fields.Char(string='Label')

    _sql_constraints = [(
        'ratio_positive',
        'CHECK(ratio >= 0)',
        'The depreciation ratio must be positive.'
        ), (
        'ratio_max',
        'CHECK(ratio <= 100)',
        'The depreciation ratio cannot be above 100%.'
        ), (
        'start_limit_days_unique',
        'unique(company_id, start_limit_days)',
        'This depreciation rule already exists in this company.'
        )]
