# Copyright 2015-2022 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import format_amount


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

    # Re-write native name_get() to use amount_untaxed instead of amount_total
    @api.depends('name', 'partner_ref', 'amount_untaxed')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' (' + po.partner_ref + ')'
            if self.env.context.get('show_total_amount') and po.amount_untaxed:
                name += ': ' + format_amount(
                    self.env, po.amount_untaxed, po.currency_id)
            result.append((po.id, name))
        return result

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


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # for optional display in tree view
    product_barcode = fields.Char(
        related='product_id.barcode', string="Product Barcode")
    product_supplier_code = fields.Char(
        compute='_compute_product_supplier_code', string='Vendor Product Code')

    def _compute_product_supplier_code(self):
        pso = self.env['product.supplierinfo']
        for line in self:
            code = False
            if not line.display_type and line.product_id and line.order_id:
                partner_id = line.order_id.partner_id.commercial_partner_id.id
                if partner_id:
                    sinfo = pso.search_read([
                        ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                        ('product_id', 'in', (False, line.product_id.id)),
                        ('partner_id', '=', partner_id),
                        ('product_code', '!=', False),
                        ('company_id', 'in', (False, line.order_id.company_id.id)),
                        ], ['product_code'], limit=1, order='product_id')
                    # if I order by product_id, I get the null values at the end
                    if sinfo:
                        code = sinfo[0]['product_code']
            line.product_supplier_code = code

    def _get_product_purchase_description(self, product_lang):
        # This is useful when you want to have the product code in a dedicated
        # column in your purchase order report
        # The same ir.config_parameter is used in sale_usability,
        # purchase_usability and account_usability
        no_product_code_param = self.env['ir.config_parameter'].sudo().get_param(
            'usability.line_name_no_product_code')
        if no_product_code_param and no_product_code_param == 'True':
            product_lang = product_lang.with_context(display_default_code=False)
        return super()._get_product_purchase_description(product_lang)

    @api.model
    def _prepare_purchase_order_line(self, product, product_qty, product_uom, company_id, supplier, po):
        # _prepare_purchase_order_line() doesn't use _get_product_purchase_description()
        # because this method is @api.model and _get_product_purchase_description() has self._ensure_one()
        # I tried to inject display_default_code in the context via super(xxx, self.with_context()),
        # but it doesn't work. That's why I rewrite vals['name']
        # The native proto uses "product_id", but it's in fact a product record set,
        # that's why I use 'product' in the proto here
        vals = super()._prepare_purchase_order_line(
            product, product_qty, product_uom, company_id, supplier, po)
        # START copy-paste from original code (I just modified product_id => product
        partner = supplier.partner_id
        uom_po_qty = product_uom._compute_quantity(product_qty, product.uom_po_id, rounding_method='HALF-UP')
        today = fields.Date.today()
        seller = product.with_company(company_id)._select_seller(
            partner_id=partner,
            quantity=uom_po_qty,
            date=po.date_order and max(po.date_order.date(), today) or today,
            uom_id=product.uom_po_id)
        # END copy-paste from original code
        product_lang = product.with_context(
            lang=partner.lang,
            partner_id=partner.id,
            seller_id=seller.id
            )
        no_product_code_param = self.env['ir.config_parameter'].sudo().get_param(
            'usability.line_name_no_product_code')
        if no_product_code_param and no_product_code_param == 'True':
            product_lang = product_lang.with_context(display_default_code=False)
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase
        vals['name'] = name
        return vals

# TODO see how we could restore this feature
#    @api.onchange('product_qty', 'product_uom')
#    def _onchange_quantity(self):
        # When the user has manually set a price and/or planned_date
        # he is often upset when Odoo changes it when he changes the qty
        # So we add a warning...
#        res = {}
#        old_price = self.price_unit
#        old_date_planned = self.date_planned
#        super()._onchange_quantity()
#        new_price = self.price_unit
#        new_date_planned = self.date_planned
#        prec = self.env['decimal.precision'].precision_get('Product Price')
#        price_compare = float_compare(old_price, new_price, precision_digits=prec)
#        if price_compare or old_date_planned != new_date_planned:
#            res['warning'] = {
#                'title': _('Updates'),
#                'message': _(
#                    "Due to the update of the ordered quantity on line '%s', "
#                    "the following data has been updated using the supplier info "
#                    "of the product:"
#                    ) % self.name
#                }
#            if price_compare:
#                res['warning']['message'] += _(
#                    "\nOld price: %s\nNew price: %s") % (
#                        format_amount(
#                            self.env, old_price, self.order_id.currency_id),
#                        format_amount(
#                            self.env, new_price, self.order_id.currency_id))

#            if old_date_planned != new_date_planned:
#                res['warning']['message'] += _(
#                    "\nOld delivery date: %s\nNew delivery date: %s") % (
#                        format_datetime(self.env, old_date_planned),
#                        format_datetime(self.env, new_date_planned),
#                    )
#        return res
