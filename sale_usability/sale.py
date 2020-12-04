# Copyright (C) 2015-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(track_visibility='onchange')
    confirmation_date = fields.Datetime(track_visibility='onchange')
    client_order_ref = fields.Char(track_visibility='onchange')
    # for partner_id, the 'sale' module sets track_visibility='always'
    partner_id = fields.Many2one(track_visibility='onchange')
    amount_tax = fields.Monetary(track_visibility='onchange')
    partner_shipping_id = fields.Many2one(track_visibility='onchange')
    partner_invoice_id = fields.Many2one(track_visibility='onchange')
    pricelist_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    # for reports
    has_discount = fields.Boolean(
        compute='_compute_has_discount', readonly=True)

    @api.depends('order_line.discount')
    def _compute_has_discount(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        for order in self:
            has_discount = False
            for line in order.order_line:
                if not float_is_zero(line.discount, precision_digits=prec):
                    has_discount = True
                    break
            order.has_discount = has_discount

    # for report
    def py3o_lines_layout(self):
        self.ensure_one()
        res = []
        has_sections = False
        subtotal = 0.0
        for line in self.order_line:
            if line.display_type == 'line_section':
                # insert line
                if has_sections:
                    res.append({'subtotal': subtotal})
                subtotal = 0.0  # reset counter
                has_sections = True
            else:
                if not line.display_type:
                    subtotal += line.price_subtotal
            res.append({'line': line})
        if has_sections:  # insert last subtotal line
            res.append({'subtotal': subtotal})
        # res:
        # [
        #    {'line': sale_order_line(1) with display_type=='line_section'},
        #    {'line': sale_order_line(2) without display_type},
        #    {'line': sale_order_line(3) without display_type},
        #    {'line': sale_order_line(4) with display_type=='line_note'},
        #    {'subtotal': 8932.23},
        # ]
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        # When the user has manually set a custom price
        # he is often upset when Odoo changes it when he changes the qty
        # So we add a warning in which we recall the old price.
        res = {}
        old_price = self.price_unit
        super().product_uom_change()
        new_price = self.price_unit
        prec = self.env['decimal.precision'].precision_get('Product Price')
        if float_compare(old_price, new_price, precision_digits=prec):
            pricelist = self.order_id.pricelist_id
            res['warning'] = {
                'title': _('Price updated'),
                'message': _(
                    "Due to the update of the ordered quantity on line '%s', "
                    "the price has been updated according to pricelist '%s'.\n"
                    "Old price: %s\n"
                    "New price: %s") % (
                        self.name,
                        pricelist.display_name,
                        formatLang(
                            self.env, old_price, currency_obj=pricelist.currency_id),
                        formatLang(
                            self.env, new_price, currency_obj=pricelist.currency_id))
                }
        return res
