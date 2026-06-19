# Copyright Akretion France (https://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import format_amount, formatLang
from markupsafe import Markup


class CommissionResult(models.Model):
    _inherit = 'commission.result'

    purchase_id = fields.Many2one('purchase.order', string="Purchase Order", tracking=True, readonly=True)

    def draft2done(self):
        for result in self:
            if result.state == "draft" and result.assign_type == 'agent':
                if not result.purchase_id:
                    vals = result._prepare_purchase_order()
                    po = self.env['purchase.order'].create(vals)
                    po.message_post(body=Markup(_("Generated from commission <a href=# data-oe-model=commission.result data-oe-id=%d>%s</a>.") % (result.id, result.display_name)))
                    result.write({'purchase_id': po.id})
                else:
                    po = self.purchase_id
                    if po.state in ('draft', 'sent', 'cancel'):
                        po.order_line.unlink()
                        po.message_post(body=Markup(_("Purchase order lines re-generated from commission <a href=# data-oe-model=commission.result data-oe-id=%d>%s</a>.") % (result.id, result.display_name)))
                    else:
                        raise UserError(_("Purchase Order %s has already been confirmed. You should cancel it first.") % po.display_name)
                    if po.state == 'cancel':
                        po.button_draft()
                assert not po.order_line
                # create lines
                line_vals = []
                if not result.company_id.commission_po_config:
                    raise UserError(_(
                        "Purchase order configuration for commission is not set on "
                        "the accounting configuration page of company '%s'.")
                        % result.company_id.display_name)
                if result.company_id.commission_po_config == 'single_line':
                    line_vals.append(result._prepare_purchase_order_line_single_line(po))
                else:
                    for move_line in result.line_ids:
                        line_vals.append(result._prepare_purchase_order_line(move_line, po))
                po_lines = self.env['purchase.order.line'].create(line_vals)
                po_lines._compute_tax_id()
        return super().draft2done()

    def _prepare_purchase_order(self):
        self.ensure_one()
        fp = self.env['account.fiscal.position'].with_company(self.company_id.id)._get_fiscal_position(self.partner_id)
        vals = {
            'partner_id': self.partner_id.id,
            'origin': _('Commission %s') % self.date_range_id.display_name,
            'company_id': self.company_id.id,
            'currency_id': self.company_id.currency_id.id,
            'fiscal_position_id': fp and fp.id or False,
            'payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
            }
        return vals

    def _prepare_purchase_order_line(self, move_line, order):
        self.ensure_one()
        move = move_line.move_id
        company_currency = move_line.company_id.currency_id
        lang = self.partner_id.lang or self.env.lang
        env = self.with_context(lang=lang).env
        product = self.profile_id.commission_product_id or self.company_id.commission_product_id
        if not product:
            raise UserError(_(
                "Commission product is not set on profile '%(profile)s' "
                "nor on company '%(company)s'.",
                profile=self.profile_id.display_name,
                company=self.company_id.display_name))
        vals = {
            'order_id': order.id,
            'product_id': product.id,
            'name': f"""{move.name} {move.commercial_partner_id.name}: {move_line.product_id.display_name} x {formatLang(env, move_line.quantity, dp='Product Unit of Measure')} {move_line.product_uom_id.display_name}\n{_('Base:')} {format_amount(env, move_line.commission_base, company_currency)} - {_('Rate:')} {formatLang(env, move_line.commission_rate, dp='Commission Rate')} %""",
            'product_qty': 1,
            'product_uom': product.uom_id.id,
            'price_unit': move_line.commission_amount,
            }
        return vals

    def _prepare_purchase_order_line_single_line(self, order):
        product = self.profile_id.commission_product_id or self.company_id.commission_product_id
        if not product:
            raise UserError(_(
                "Commission product is not set on profile '%(profile)s' "
                "nor on company '%(company)s'.",
                profile=self.profile_id.display_name,
                company=self.company_id.display_name))
        vals = {
            'order_id': order.id,
            'product_id': product.id,
            'name': _("Commissions for period %(period)s", period=self.date_range_id.name),
            'product_qty': 1,
            'product_uom': product.uom_id.id,
            'price_unit': self.amount_total,
            }
        return vals

    def unlink(self):
        for result in self:
            if result.purchase_id:
                raise UserError(_(
                    "Cannot delete commission %(commission)s because it is linked to "
                    "purchase order %(po)s. You must delete the purchase order first.",
                    commission=result.display_name, po=result.purchase_id.display_name))
        return super().unlink()
