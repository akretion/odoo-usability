# -*- coding: utf-8 -*-
# Copyright (C) 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Also defined in bi_sale_company_currency
    company_currency_id = fields.Many2one(
        related='order_id.company_id.currency_id',
        readonly=True, store=True, string='Company Currency')
    standard_price_company_currency = fields.Float(
        string='Cost Price in Company Currency', readonly=True,
        digits=dp.get_precision('Product Price'),
        help="Cost price in company currency in the unit of measure "
        "of the sale order line")
    standard_price_sale_currency = fields.Float(
        string='Cost Price in Sale Currency', readonly=True,
        compute='_compute_margin', store=True,
        digits=dp.get_precision('Product Price'),
        help="Cost price in sale currency in the unit of measure "
        "of the sale order line")
    margin_sale_currency = fields.Monetary(
        string='Margin in Sale Currency', readonly=True, store=True,
        compute='_compute_margin', currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency', readonly=True, store=True,
        compute='_compute_margin', currency_field='company_currency_id')
    margin_rate = fields.Float(
        string="Margin (%)", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.depends(
        'standard_price_company_currency', 'order_id.pricelist_id.currency_id',
        'order_id.date_order', 'product_uom_qty', 'price_subtotal',
        'order_id.company_id')
    def _compute_margin(self):
        for line in self:
            standard_price_sale_cur = 0.0
            margin_sale_cur = 0.0
            margin_comp_cur = 0.0
            margin_rate = 0.0
            order_cur = line.order_id.pricelist_id.currency_id
            company_cur = line.order_id.company_id.currency_id
            if order_cur and company_cur:
                date = line.order_id.date_order
                standard_price_sale_cur =\
                    company_cur.with_context(date=date).compute(
                        line.standard_price_company_currency, order_cur)
                margin_sale_cur =\
                    line.price_subtotal\
                    - line.product_uom_qty * standard_price_sale_cur
                margin_comp_cur = order_cur.with_context(date=date).compute(
                    margin_sale_cur, company_cur)
                if line.price_subtotal:
                    margin_rate = 100 * margin_sale_cur / line.price_subtotal
            line.standard_price_sale_currency = standard_price_sale_cur
            line.margin_sale_currency = margin_sale_cur
            line.margin_company_currency = margin_comp_cur
            line.margin_rate = margin_rate

    # We want to copy standard_price on sale order line
    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            pp = self.env['product.product'].browse(vals['product_id'])
            std_price = pp.standard_price
            sale_uom_id = vals.get('product_uom')
            if sale_uom_id and sale_uom_id != pp.uom_id.id:
                sale_uom = self.env['product.uom'].browse(sale_uom_id)
                # convert from product UoM to sale UoM
                std_price = pp.uom_id._compute_price(
                    standard_price, sale_uom)
            vals['standard_price_company_currency'] = std_price
        return super(SaleOrderLine, self).create(vals)

    def write(self, vals):
        if not vals:
            vals = {}
        if 'product_id' in vals or 'product_uom' in vals:
            for sol in self:
                # product_uom and product_id are required fields
                if 'product_id' in vals:
                    pp = self.env['product.product'].browse(vals['product_id'])
                else:
                    pp = sol.product_id
                if 'product_uom' in vals:
                    sale_uom = self.env['product.uom'].browse(
                        vals['product_uom'])
                else:
                    sale_uom = sol.product_uom
                std_price = pp.standard_price
                if sale_uom != pp.uom_id:
                    std_price = pp.uom_id._compute_price(std_price, sale_uom)
                sol.write({'standard_price_company_currency': std_price})
        return super(SaleOrderLine, self).write(vals)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Also defined in bi_sale_company_currency
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True, store=True,
        string="Company Currency")
    margin_sale_currency = fields.Monetary(
        string='Margin in Sale Currency',
        currency_field='currency_id',
        readonly=True, compute='_compute_margin', store=True)
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency',
        currency_field='company_currency_id',
        readonly=True, compute='_compute_margin', store=True)

    @api.depends(
        'order_line.margin_sale_currency',
        'order_line.margin_company_currency')
    def _compute_margin(self):
        for order in self:
            margin_sale_cur = 0.0
            margin_comp_cur = 0.0
            for sol in order.order_line:
                margin_sale_cur += sol.margin_sale_currency
                margin_comp_cur += sol.margin_company_currency
            order.margin_sale_currency = margin_sale_cur
            order.margin_company_currency = margin_comp_cur
