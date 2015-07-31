# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Margin No Onchange module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    standard_price_company_currency = fields.Float(
        string='Cost Price in Company Currency', readonly=True,
        digits=dp.get_precision('Product Price'))
    standard_price_sale_currency = fields.Float(
        string='Cost Price in Sale Currency', readonly=True,
        compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))
    margin_sale_currency = fields.Float(
        string='Margin in Sale Currency', readonly=True, store=True,
        compute='_compute_margin',
        digits=dp.get_precision('Account'))
    margin_company_currency = fields.Float(
        string='Margin in Company Currency', readonly=True, store=True,
        compute='_compute_margin',
        digits=dp.get_precision('Account'))
    margin_rate = fields.Float(
        string="Margin Rate", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.one
    @api.depends(
        'standard_price_company_currency', 'order_id.pricelist_id',
        'order_id.date_order', 'product_uom_qty', 'price_subtotal')
    def _compute_margin(self):
        standard_price_sale_cur = 0.0
        margin_sale_cur = 0.0
        margin_comp_cur = 0.0
        margin_rate = 0.0
        if self.order_id and self.order_id.currency_id:
            # it works in _get_current_rate
            # even if we set date = False in context
            standard_price_sale_cur =\
                self.order_id.company_id.currency_id.with_context(
                    date=self.order_id.date_order).compute(
                        self.standard_price_company_currency,
                        self.order_id.currency_id)
            margin_sale_cur =\
                self.price_subtotal\
                - self.product_uom_qty * standard_price_sale_cur
            margin_comp_cur = self.order_id.currency_id.with_context(
                date=self.order_id.date_order).compute(
                    margin_sale_cur, self.order_id.company_id.currency_id)
            if self.price_subtotal:
                margin_rate = 100 * margin_sale_cur / self.price_subtotal
        self.standard_price_sale_currency = standard_price_sale_cur
        self.margin_sale_currency = margin_sale_cur
        self.margin_company_currency = margin_comp_cur
        self.margin_rate = margin_rate

    # We want to copy standard_price on sale order line
    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            pp = self.env['product.product'].browse(vals['product_id'])
            std_price = pp.standard_price
            sale_uom_id = vals.get('product_uom')
            if sale_uom_id and sale_uom_id != pp.uom_id.id:
                std_price = self.env['product.uom']._compute_price(
                    pp.uom_id.id, std_price, sale_uom_id)
            vals['standard_price_company_currency'] = std_price
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    def write(self, vals):
        if not vals:
            vals = {}
        if 'product_id' in vals or 'product_uom' in vals:
            for sol in self:
                if 'product_id' in vals:
                    if vals.get('product_id'):
                        pp = self.env['product.product'].browse(
                            vals['product_id'])
                    else:
                        pp = False
                else:
                    pp = sol.product_id or False
                # product_uom is a required field,
                # so it's different from product_id
                if 'product_uom' in vals:
                    sale_uom = self.env['product.uom'].browse(
                        vals['product_uom'])
                else:
                    sale_uom = sol.product_uom
                std_price = 0.0
                if pp:
                    std_price = pp.standard_price
                    if sale_uom != pp.uom_id:
                        std_price = self.env['product.uom']._compute_price(
                            pp.uom_id.id, std_price, sale_uom.id)
                sol.write({'standard_price_company_currency': std_price})
        return super(SaleOrderLine, self).write(vals)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    margin_sale_currency = fields.Float(
        string='Margin in Sale Currency',
        readonly=True, compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))
    margin_company_currency = fields.Float(
        string='Margin in Company Currency',
        readonly=True, compute='_compute_margin', store=True,
        digits=dp.get_precision('Account'))

    @api.one
    @api.depends(
        'order_line.margin_sale_currency',
        'order_line.margin_company_currency')
    def _compute_margin(self):
        margin_sale_cur = 0.0
        margin_comp_cur = 0.0
        for sol in self.order_line:
            margin_sale_cur += sol.margin_sale_currency
            margin_comp_cur += sol.margin_company_currency
        self.margin_sale_currency = margin_sale_cur
        self.margin_company_currency = margin_comp_cur
