# Copyright 2015-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    standard_price_company_currency = fields.Float(
        string='Unit Cost Price in Company Currency', readonly=True,
        digits='Product Price',
        help="Unit Cost price in company currency in the unit of measure "
        "of the invoice line (which may be different from the unit "
        "of measure of the product).")
    standard_price_invoice_currency = fields.Float(
        string='Unit Cost Price in Invoice Currency',
        compute='_compute_margin', store=True, digits='Product Price',
        help="Unit Cost price in invoice currency in the unit of measure "
        "of the invoice line.")
    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency', store=True,
        compute='_compute_margin', currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency', store=True,
        compute='_compute_margin', currency_field='company_currency_id')
    margin_rate = fields.Float(
        string="Margin Rate", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.depends(
        'standard_price_company_currency', 'move_id.currency_id',
        'move_id.move_type', 'move_id.company_id',
        'move_id.invoice_date', 'quantity', 'price_subtotal')
    def _compute_margin(self):
        for ml in self:
            standard_price_inv_cur = 0.0
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            margin_rate = 0.0
            move = ml.move_id
            if move.move_type and move.move_type in ('out_invoice', 'out_refund'):
                # it works in _get_current_rate
                # even if we set date = False in context
                # standard_price_inv_cur is in the UoM of the invoice line
                date = move.date or fields.Date.context_today(self)
                company = move.company_id
                company_currency = company.currency_id
                standard_price_inv_cur =\
                    company_currency._convert(
                        ml.standard_price_company_currency,
                        ml.currency_id, company, date)
                margin_inv_cur =\
                    ml.price_subtotal - ml.quantity * standard_price_inv_cur
                margin_comp_cur = move.currency_id._convert(
                    margin_inv_cur, company_currency, company, date)
                if ml.price_subtotal:
                    margin_rate = 100 * margin_inv_cur / ml.price_subtotal
                # for a refund, margin should be negative
                # but margin rate should stay positive
                if move.move_type == 'out_refund':
                    margin_inv_cur *= -1
                    margin_comp_cur *= -1
            ml.standard_price_invoice_currency = standard_price_inv_cur
            ml.margin_invoice_currency = margin_inv_cur
            ml.margin_company_currency = margin_comp_cur
            ml.margin_rate = margin_rate

    # We want to copy standard_price on invoice line for customer
    # invoice/refunds. We can't do that via on_change of product_id,
    # because it is not always played when invoice is created from code
    # => we inherit write/create
    # We write standard_price_company_currency even on supplier invoice/refunds
    # because we don't have access to the 'type' of the invoice
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('product_id') and not vals.get('display_type'):
                pp = self.env['product.product'].browse(vals['product_id'])
                std_price = pp.standard_price
                inv_uom_id = vals.get('product_uom_id')
                if inv_uom_id and inv_uom_id != pp.uom_id.id:
                    inv_uom = self.env['uom.uom'].browse(inv_uom_id)
                    std_price = pp.uom_id._compute_price(
                        std_price, inv_uom)
                vals['standard_price_company_currency'] = std_price
        return super().create(vals_list)

    def write(self, vals):
        if not vals:
            vals = {}
        if 'product_id' in vals or 'product_uom_id' in vals:
            for il in self:
                if 'product_id' in vals:
                    if vals.get('product_id'):
                        pp = self.env['product.product'].browse(
                            vals['product_id'])
                    else:
                        pp = False
                else:
                    pp = il.product_id or False
                # uom_id is NOT a required field
                if 'product_uom_id' in vals:
                    if vals.get('product_uom_id'):
                        inv_uom = self.env['uom.uom'].browse(
                            vals['product_uom_id'])
                    else:
                        inv_uom = False
                else:
                    inv_uom = il.uom_id or False
                std_price = 0.0
                if pp:
                    std_price = pp.standard_price
                    if inv_uom and inv_uom != pp.uom_id:
                        std_price = pp.uom_id._compute_price(
                            std_price, inv_uom)
                il.write({'standard_price_company_currency': std_price})
        return super().write(vals)


class AccountMove(models.Model):
    _inherit = 'account.move'

    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency',
        compute='_compute_margin', store=True,
        currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency',
        compute='_compute_margin', store=True,
        currency_field='company_currency_id')

    @api.depends(
        'move_type',
        'invoice_line_ids.margin_invoice_currency',
        'invoice_line_ids.margin_company_currency')
    def _compute_margin(self):
        rg_res = self.env['account.move.line'].read_group(
            [
                ('move_id', 'in', self.ids),
                ('display_type', '=', False),
                ('exclude_from_invoice_tab', '=', False),
                ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
            ],
            ['move_id', 'margin_invoice_currency:sum', 'margin_company_currency:sum'],
            ['move_id'])
        mapped_data = dict([(x['move_id'][0], {
            'margin_invoice_currency': x['margin_invoice_currency'],
            'margin_company_currency': x['margin_company_currency'],
            }) for x in rg_res])
        for move in self:
            move.margin_invoice_currency = mapped_data.get(move.id, {}).get('margin_invoice_currency')
            move.margin_company_currency = mapped_data.get(move.id, {}).get('margin_company_currency')
