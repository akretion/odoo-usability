# -*- coding: utf-8 -*-
# Copyright 2015-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools.misc import formatLang
from odoo.tools import float_compare


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dest_address_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    partner_ref = fields.Char(track_visibility='onchange')
    # field 'partner_id': native value for track_visibility='always'
    partner_id = fields.Many2one(track_visibility='onchange')
    # the field 'delivery_partner_id' is used in report
    # the compute method of that field is inherited in purchase_stock_usability
    delivery_partner_id = fields.Many2one(
        'res.partner', compute='_compute_delivery_partner_id', readonly=True)

    @api.depends('dest_address_id')
    def _compute_delivery_partner_id(self):
        for order in self:
            order.delivery_partner_id = order.dest_address_id

    def print_order(self):
        report = self.env.ref('purchase.action_report_purchase_order')
        action = report.report_action(self)
        return action

    # Re-write native name_get() to use amount_untaxed instead of amount_total
    @api.multi
    @api.depends('name', 'partner_ref')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' (' + po.partner_ref + ')'
            if self.env.context.get('show_total_amount') and po.amount_total:
                name += ': ' + formatLang(
                    self.env, po.amount_untaxed, currency_obj=po.currency_id)
            result.append((po.id, name))
        return result


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_qty', 'product_uom')
    def _onchange_quantity(self):
        # When the user has manually set a price and/or planned_date
        # he is often upset when Odoo changes it when he changes the qty
        # So we add a warning...
        res = {}
        old_price = self.price_unit
        old_date_planned = self.date_planned
        super()._onchange_quantity()
        new_price = self.price_unit
        new_date_planned = self.date_planned
        prec = self.env['decimal.precision'].precision_get('Product Price')
        price_compare = float_compare(old_price, new_price, precision_digits=prec)
        if price_compare or old_date_planned != new_date_planned:
            res['warning'] = {
                'title': _('Updates'),
                'message': _(
                    "Due to the update of the ordered quantity on line '%s', "
                    "the following data has been updated using the supplier info "
                    "of the product:"
                    ) % self.name
                }
            if price_compare:
                res['warning']['message'] += _(
                    "\nOld price: %s\nNew price: %s") % (
                        formatLang(
                            self.env, old_price,
                            currency_obj=self.order_id.currency_id),
                        formatLang(
                            self.env, new_price,
                            currency_obj=self.order_id.currency_id))

            if old_date_planned != new_date_planned:
                res['warning']['message'] += _(
                    "\nOld delivery date: %s\nNew delivery date: %s") % (
                        old_date_planned,
                        new_date_planned,
                    )
        return res
