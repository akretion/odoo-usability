# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    sale_order_count = fields.Integer(
        compute='compute_sale_order_count',
        string='Number of Quotations/Orders', readonly=True)
    sale_ids = fields.One2many(
        'sale.order', 'project_id', string='Quotations/Orders')

    @api.multi
    def compute_sale_order_count(self):
        for aaa in self:
            try:
                count = len(aaa.sale_ids)
            except:
                count = 0
            aaa.sale_order_count = count
