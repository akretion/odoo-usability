# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class LunchVoucherAttribution(models.Model):
    _name = 'lunch.voucher.attribution'
    _description = 'Lunch Voucher Attribution'
    _order = 'date desc'

    employee_id = fields.Many2one(
        'hr.employee', string='Employee', ondelete='restrict',
        required=True, readonly=True)
    company_id = fields.Many2one(
        related='employee_id.resource_id.company_id', readonly=True,
        store=True)
    date = fields.Date('Attribution Date', readonly=True)
    purchase_id = fields.Many2one(
        'purchase.order', 'Purchase Order',
        readonly=True)
    month_work_days = fields.Integer(
        'Month Work Days',
        help="Number of work days of the month (without taking into "
        "account the holidays)")
    no_lunch_days = fields.Integer(
        compute='_compute_qty', string='No Lunch Days',
        readonly=True, store=True)
    qty = fields.Integer(
        compute='_compute_qty', readonly=True, store=True,
        string='Lunch Voucher Quantity')
    holiday_ids = fields.One2many(
        'hr.holidays', 'lunch_voucher_id', readonly=True)

    @api.depends('month_work_days', 'holiday_ids.lunch_voucher_remove_qty')
    def _compute_qty(self):
        for rec in self:
            no_lunch_days = 0
            for hol in rec.holiday_ids:
                no_lunch_days += hol.lunch_voucher_remove_qty
            rec.no_lunch_days = no_lunch_days
            rec.qty = rec.month_work_days - no_lunch_days
