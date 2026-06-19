# Copyright 2019-2024 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.tools import float_is_zero


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    commission_result_id = fields.Many2one(
        'commission.result', string='Commission Result', check_company=True, index=True, copy=False)
    commission_rule_id = fields.Many2one(
        'commission.rule', 'Matched Commission Rule', ondelete='restrict', check_company=True, copy=False)
    commission_base = fields.Monetary('Commission Base', currency_field='company_currency_id', copy=False)
    commission_rate = fields.Float('Commission Rate', digits='Commission Rate', copy=False)
    commission_amount = fields.Monetary(
        string='Commission Amount', currency_field='company_currency_id',
        readonly=True, compute='_compute_commission_amount', store=True)
    # to display on commission line
    product_categ_id = fields.Many2one(
        related='product_id.product_tmpl_id.categ_id')

    @api.depends('commission_rate', 'commission_base')
    def _compute_commission_amount(self):
        for line in self:
            commission_amount = False
            if line.display_type == 'product':
                commission_amount = line.company_currency_id.round(
                    line.commission_rate * line.commission_base / 100.0)
            line.commission_amount = commission_amount

    def _match_commission_rule(self, rules):
        # commission rules are already in the right order
        self.ensure_one()
        for rule in rules:
            if rule['date_start'] and rule['date_start'] > self.date:
                continue
            if rule['date_end'] and rule['date_end'] < self.date:
                continue
            if rule['applied_on'] == '0_customer_product':
                if (
                        self.partner_id.id in
                        rule['partner_ids'] and
                        self.product_id.id in rule['product_ids']):
                    return rule
            elif rule['applied_on'] == '1_customer_product_category':
                if (
                        self.partner_id.id in
                        rule['partner_ids'] and
                        self.product_categ_id.id in rule['product_categ_ids']):
                    return rule
            elif rule['applied_on'] == '2_product':
                if self.product_id.id in rule['product_ids']:
                    return rule
            elif rule['applied_on'] == '3_product_category':
                if self.product_categ_id.id in rule['product_categ_ids']:
                    return rule
            elif rule['applied_on'] == '4_global':
                return rule
        return False

    def _prepare_commission_data(self, rule):
        self.ensure_one()
        rate_prec = self.env['decimal.precision'].precision_get('Commission Rate')
        lvals = {
            'commission_rule_id': rule['id'],
            # company currency
            # inherit this method to change the value below if you want to base on margin
            # or something else
            'commission_rate': rule['rate'],
            }
        if rule['base'] == 'margin':
            # What do we do if it's negative ? For the moment, it adds a negative commission line
            cost = 0
            if self.product_id and self.product_uom_id:
                # if the module account_invoice_margin from akretion/odoo-usability is installed
                if hasattr(self, 'margin_company_currency'):
                    cost = self.margin_company_currency
                else:
                    sign = self.move_id.move_type == 'out_refund' and -1 or 1
                    cost = self.product_id.standard_price * self.product_uom_id._compute_quantity(self.quantity, self.product_id.uom_id) * sign
            lvals['commission_base'] = self.balance * -1 - cost
        else:
            lvals['commission_base'] = self.balance * -1
        if float_is_zero(lvals['commission_rate'], precision_digits=rate_prec) or self.company_currency_id.is_zero(lvals['commission_base']):
            return False
        return lvals

    def _prepare_commission_xlsx(self):
        self.ensure_one()
        vals = {
            "inv.name": self.move_id.name,
            "inv.date": self.move_id.invoice_date,
            "inv.partner": self.move_id.commercial_partner_id.display_name,
            "product": self.product_id and self.product_id.display_name or self.name,
            "qty": self.quantity,
            "uom": self.product_uom_id.name,
            "commission_base": self.commission_base,
            "commission_rate": self.commission_rate / 100,
            "commission_amount": self.commission_amount,
        }
        return vals
