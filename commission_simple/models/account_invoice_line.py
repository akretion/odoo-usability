# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
import odoo.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    user_id = fields.Many2one(
        related='invoice_id.user_id', store=True, readonly=True)
    product_categ_id = fields.Many2one(
        related='product_id.product_tmpl_id.categ_id', store=True, readonly=True)
    commission_result_id = fields.Many2one(
        'commission.result', string='Commission Result')
    commission_rule_id = fields.Many2one(
        'commission.rule', 'Matched Commission Rule', ondelete='restrict')
    commission_base = fields.Monetary('Commission Base', currency_field='company_currency_id')
    commission_rate = fields.Float('Commission Rate', digits=dp.get_precision('Commission Rate'))
    commission_amount = fields.Monetary(
        string='Commission Amount', currency_field='company_currency_id',
        readonly=True, compute='_compute_commission_amount', store=True)

    @api.depends('commission_rate', 'commission_base')
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = line.company_currency_id.round(
                line.commission_rate * line.commission_base / 100.0)

    def compute_commission_for_one_user(self, user, date_range, rules):
        profile = user.commission_profile_id
        company = profile.company_id
        company_currency = company.currency_id
        assert profile
        domain = [
            ('invoice_type', 'in', ('out_invoice', 'out_refund')),
            ('date_invoice', '<=', date_range.date_end),
            ('company_id', '=', company.id),
            ('user_id', '=', user.id),
            ('commission_result_id', '=', False),
            ]
        if profile.trigger_type == 'invoice':
            domain.append(('state', 'in', ('open', 'paid')))
        elif profile.trigger_type == 'payment':
            # TODO : for this trigger, we would need to filter
            # out the invoices paid after the end date of the period compute
            domain.append(('state', '=', 'paid'))
        else:
            raise
        ilines = self.search(domain, order='date_invoice, invoice_id, sequence')
        com_result = self.env['commission.result'].create({
            'user_id': user.id,
            'profile_id': profile.id,
            'date_range_id': date_range.id,
            })
        total = 0.0
        for iline in ilines:
            rule = iline._match_commission_rule(rules[profile.id])
            if rule:
                lvals = iline._prepare_commission_data(rule, com_result)
                if lvals:
                    iline.write(lvals)
                    total += company_currency.round(
                        lvals['commission_rate'] * lvals['commission_base']
                        / 100.0)
        com_result.amount_total = total
        return com_result

    def _match_commission_rule(self, rules):
        # commission rules are already in the right order
        self.ensure_one()
        for rule in rules:
            if rule['date_start'] and rule['date_start'] > self.date_invoice:
                continue
            if rule['date_end'] and rule['date_end'] < self.date_invoice:
                continue
            if rule['applied_on'] == '0_customer_product':
                if (
                        self.commercial_partner_id.id in
                        rule['partner_ids'] and
                        self.product_id.id in rule['product_ids']):
                    return rule
            elif rule['applied_on'] == '1_customer_product_category':
                if (
                        self.commercial_partner_id.id in
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

    def _prepare_commission_data(self, rule, commission_result):
        self.ensure_one()
        lvals = {
            'commission_result_id': commission_result.id,
            'commission_rule_id': rule['id'],
            # company currency
            'commission_base': self.price_subtotal_signed,
            'commission_rate': rule['rate'],
            }
        return lvals
