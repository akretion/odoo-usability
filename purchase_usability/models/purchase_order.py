# Copyright 2015-2020 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.misc import formatLang
from odoo.tools import float_is_zero


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
    product_barcode = fields.Char(related='product_id.barcode', string="Product Barcode")
    invoice_status = fields.Selection(
        [
            ("no", "Nothing to Bill"),
            ("to invoice", "Waiting Bills"),
            ("invoiced", "Fully Billed"),
        ],
        string="Billing Status",
        compute="_compute_invoice_status",
        store=True,
        readonly=True,
        default="no",
    )

    @api.depends("state", "qty_to_invoice", "qty_invoiced")
    def _compute_invoice_status(self):
        """Mimic PO '_get_invoiced' method to compute PO line invoice status"""
        prec = self.env["decimal.precision"].precision_get("Product Unit of Measure")
        for line in self:
            if line.state not in ("purchase", "done") or line.display_type:
                line.invoice_status = "no"
                continue

            if not float_is_zero(line.qty_to_invoice, precision_digits=prec):
                line.invoice_status = "to invoice"
            elif float_is_zero(
                line.qty_to_invoice, precision_digits=prec
            ) and not float_is_zero(line.qty_invoiced, precision_digits=prec):
                line.invoice_status = "invoiced"
            else:
                line.invoice_status = "no"
