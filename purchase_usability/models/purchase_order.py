# Copyright 2015-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import formatLang


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dest_address_id = fields.Many2one(tracking=True)
    currency_id = fields.Many2one(tracking=True)
    payment_term_id = fields.Many2one(tracking=True)
    fiscal_position_id = fields.Many2one(tracking=True)
    partner_ref = fields.Char(tracking=True)
    # the field 'delivery_partner_id' is used in report
    # the compute method of that field is inherited in purchase_stock_usability
    delivery_partner_id = fields.Many2one(
        'res.partner', compute='_compute_delivery_partner_id')

    @api.depends('dest_address_id')
    def _compute_delivery_partner_id(self):
        for order in self:
            order.delivery_partner_id = order.dest_address_id

    def print_order(self):
        report = self.env.ref('purchase.action_report_purchase_order')
        action = report.report_action(self)
        return action

    # Re-write native name_get() to use amount_untaxed instead of amount_total
    @api.depends('name', 'partner_ref')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' (' + po.partner_ref + ')'
            if self.env.context.get('show_total_amount') and po.amount_untaxed:
                name += ': ' + formatLang(
                    self.env, po.amount_untaxed, currency_obj=po.currency_id)
            result.append((po.id, name))
        return result
