# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.tools import float_compare
from odoo.exceptions import UserError


class SaleInvoiceDiscountAllLines(models.TransientModel):
    _name = 'sale.invoice.discount.all.lines'
    _description = 'Apply discount on all lines of a sale order or invoice'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if self._context.get('active_id'):
            if self._context.get('active_model') == 'sale.order':
                res['sale_id'] = self._context['active_id']
            elif self._context.get('active_model') == 'account.move':
                res['move_id'] = self._context['active_id']
                move = self.env['account.move'].browse(res['move_id'])
                if move.state != 'draft':
                    raise UserError(
                        _("Invoice '%s' is not in draft state.")
                        % self.move_id.display_name)
            else:
                # I don't translate this because it should never happen.
                raise UserError(
                    "This wizard can only work on a sale order or an invoice.")
        else:
            # I don't translate this because it should never happen.
            raise UserError("Missing active_id in context. It should never happen.")
        return res

    sale_id = fields.Many2one(
        'sale.order', string='Order', readonly=True)
    move_id = fields.Many2one(
        'account.move', string='Invoice', readonly=True)
    discount = fields.Float(
        string='Discount', digits='Discount', required=True)
    line_type = fields.Selection([
        ('all', 'All Lines'),
        ('products', 'All Product Lines'),
        ('services', 'All Service Lines'),
        ], default='all', required=True, string='Apply on')

    def run(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        if float_compare(self.discount, 0, precision_digits=prec) < 0:
            raise UserError(_("Discount cannot be negative."))
        if self.sale_id:
            record = self.sale_id
            line_obj = self.env['sale.order.line']
            domain = [('order_id', '=', self.sale_id.id)]
        elif self.move_id:
            record = self.move_id
            if self.move_id.state != 'draft':
                raise UserError(_(
                    "Invoice '%s' is not in draft state.") % self.move_id.display_name)
            line_obj = self.env['account.move.line']
            domain = [
                ('move_id', '=', self.move_id.id),
                ('exclude_from_invoice_tab', '=', False),
                ]
        else:
            # I don't translate this because it should never happen.
            raise UserError(
                "The wizard is not linked to a sale order nor an invoice. "
                "This should never happen.")
        domain += [('display_type', '=', False)]
        if self.line_type == 'products':
            domain += [
                ('product_id', '!=', False),
                ('product_id.type', '!=', 'service'),
                ]
        elif self.line_type == 'services':
            domain += [
                ('product_id', '!=', False),
                ('product_id.type', '=', 'service'),
                ]
        lines = line_obj.search(domain)
        if not lines:
            raise UserError(_("There are no lines to apply the discount on."))
        lines.with_context(check_move_validity=False).write({'discount': self.discount})
        if self.move_id:
            self.move_id.with_context(
                check_move_validity=False)._recompute_dynamic_lines(
                    recompute_all_taxes=True)
            self.move_id._check_balanced()
        record.message_post(body=_(
            "Applied a {discount}% discount on {line_type}.").format(
                discount=self.discount,
                line_type=self._fields['line_type'].convert_to_export(
                    self.line_type, self)))
