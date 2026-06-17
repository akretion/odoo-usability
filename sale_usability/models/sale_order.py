# Copyright (C) 2015-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_order = fields.Datetime(tracking=True)
    client_order_ref = fields.Char(tracking=True)
    # for partner_id, the 'sale' module sets track_visibility='always'
    amount_tax = fields.Monetary(tracking=True)
    partner_shipping_id = fields.Many2one(tracking=True)
    partner_invoice_id = fields.Many2one(tracking=True)
    pricelist_id = fields.Many2one(tracking=True)
    payment_term_id = fields.Many2one(tracking=True)
    fiscal_position_id = fields.Many2one(tracking=True)
    # for reports
    has_discount = fields.Boolean(compute='_compute_has_discount')
    has_attachment = fields.Boolean(
        compute='_compute_has_attachment',
        search='_search_has_attachment')

    @api.depends('order_line.discount')
    def _compute_has_discount(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        for order in self:
            has_discount = False
            for line in order.order_line:
                if not line.display_type and not float_is_zero(
                        line.discount, precision_digits=prec):
                    has_discount = True
                    break
            order.has_discount = has_discount

    def _compute_has_attachment(self):
        iao = self.env['ir.attachment']
        for order in self:
            if iao.search_count([
                    ('res_model', '=', 'sale.order'),
                    ('res_id', '=', order.id),
                    ('type', '=', 'binary'),
                    ('company_id', '=', order.company_id.id)]):
                order.has_attachment = True
            else:
                order.has_attachment = False

    def _search_has_attachment(self, operator, value):
        att_order_ids = {}
        if operator == '=':
            search_res = self.env['ir.attachment'].search_read([
                ('res_model', '=', 'sale.order'),
                ('type', '=', 'binary'),
                ('res_id', '!=', False)], ['res_id'])
            for att in search_res:
                att_order_ids[att['res_id']] = True
        res = [('id', value and 'in' or 'not in', list(att_order_ids))]
        return res

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
            elif not line.display_type:
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

    # for optional display in tree view
    product_barcode = fields.Char(
        related='product_id.barcode', string="Product Barcode")

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        # When the user has manually set a custom price
        # he is often upset when Odoo changes it when he changes the qty
        # So we add a warning in which we recall the old price.
        PricelistItem = self.env['product.pricelist.item']
        res = {}
        old_price = self.price_unit
        super().product_uom_change()
        new_price = self.price_unit
        pricelist_item = PricelistItem.browse(False)
        if self.product_id:
            product_context = dict(self.env.context,
                                   partner_id=self.order_id.partner_id.id,
                                   date=self.order_id.date_order,
                                   uom=self.product_uom.id)
            price, rule_id = self.order_id.pricelist_id.with_context(
                product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
            pricelist_item = PricelistItem.browse(rule_id)
        prec = self.env['decimal.precision'].precision_get('Product Price')
        if pricelist_item.base != 'supplierinfo' and float_compare(old_price, new_price, precision_digits=prec):
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

    def get_sale_order_line_multiline_description_sale(self, product):
        # This is useful when you want to have the product code in a dedicated
        # column in your sale order report
        # The same ir.config_parameter is used in sale_usability,
        # purchase_usability and account_usability
        no_product_code_param = self.env['ir.config_parameter'].sudo().get_param(
            'usability.line_name_no_product_code')
        if no_product_code_param and no_product_code_param == 'True':
            product = product.with_context(display_default_code=False)
        return super().get_sale_order_line_multiline_description_sale(product)

    # In v12, I developped the 3 modules service_line_qty_update_base, service_line_qty_update_purchase
    # and service_line_qty_update_sale that add a wizard to update service lines and track the changes
    # in the chatter.
    # In v14, you can edit the quantity of the service lines directly and the purchase module
    # tracks changes in the chatter... but the sale module doesn't track the changes of 'qty_delivered'
    # So I "ported" that native feature of the purchase module to sale.order.line... here it is !
    # We can remove that code if this feature is added in the sale module (it's NOT the case in
    # odoo v17)
    def write(self, vals):
        if 'qty_delivered' in vals:
            for line in self:
                line._track_qty_delivered(vals['qty_delivered'])
        return super().write(vals)

    def _track_qty_delivered(self, new_qty):
        self.ensure_one()
        prec = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        if (
                float_compare(new_qty, self.qty_delivered, precision_digits=prec) and
                self.order_id.state == 'sale'):
            self.order_id.message_post_with_view(
                'sale_usability.track_so_line_qty_delivered_template',
                values={'line': self, 'qty_delivered': new_qty},
                subtype_id=self.env.ref('mail.mt_note').id
            )
