# -*- coding: utf-8 -*-
# © 2014-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # same code in class product.product and product.template
    @api.onchange('can_be_expensed')
    def onchange_can_be_expensed(self):
        if self.can_be_expensed:
            unit_uom = self.env.ref('product.product_uom_unit')
            self.type = 'service'
            self.list_price = 0.0
            self.sale_ok = False
            self.purchase_ok = False
            self.uom_id = unit_uom.id
            self.po_uom_id = unit_uom.id
            self.taxes_id = False

    # It probably doesn't make sense to have a constraint on a property fields
    # But the same constrain is also on hr.expense
    @api.constrains('supplier_taxes_id', 'can_be_expensed')
    def _check_expense_product(self):
        for product in self:
            if product.can_be_expensed and product.supplier_taxes_id:
                if len(product.supplier_taxes_id) > 1:
                    raise ValidationError(_(
                        "The module hr_expense_usability only supports one "
                        "tax for expense products. The product '%s' has "
                        "more than one tax.") % product.display_name)
                if not product.supplier_taxes_id[0].price_include:
                    raise ValidationError(_(
                        "The module hr_expense_usability only supports "
                        "taxes with the property 'Included in Price' for "
                        "expense products. The tax '%s' on the product '%s' "
                        "is not 'Included in Price'.") % (
                        product.supplier_taxes_id[0].name,
                        product.display_name))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # same code in class product.product and product.template
    @api.onchange('can_be_expensed')
    def onchange_can_be_expensed(self):
        if self.can_be_expensed:
            unit_uom = self.env.ref('product.product_uom_unit')
            self.type = 'service'
            self.list_price = 0.0
            self.sale_ok = False
            self.purchase_ok = False
            self.uom_id = unit_uom.id
            self.po_uom_id = unit_uom.id
            self.taxes_id = False


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def _get_accounting_partner_from_employee(self):
        # By default, odoo uses self.employee_id.address_home_id
        # which users usually don't configure
        # (even demo data doesn't bother to set it...)
        # So I decided to put a fallback on employee.user_id.partner_id
        self.ensure_one()
        if self.address_home_id:
            partner = self.address_home_id.commercial_partner_id
        elif self.user_id:
            # We don't use "commercial partner" here...
            partner = self.user_id.partner_id
        else:
            raise UserError(_(
                "The employee '%s' doesn't have a Home Address and isn't "
                "linked to an Odoo user. You have to set one of these two "
                "fields on the employee form in order to get a partner from "
                "the employee for the Journal Items.") % self.display_name)
        return partner


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    employee_id = fields.Many2one(track_visibility='onchange')
    date = fields.Date(track_visibility='onchange', required=True)
    currency_id = fields.Many2one(track_visibility='onchange', required=True)
    total_amount = fields.Float(track_visibility='onchange')
    # I want a specific precision for unit_amount of expense
    # main reason is KM cost which is 3 by default
    unit_amount = fields.Float(digits=dp.get_precision('Expense Unit Price'))
    tax_amount = fields.Monetary(
        string='Tax Amount', currency_field='currency_id',
        readonly=True, states={'draft': [('readonly', False)]})
    untaxed_amount_usability = fields.Monetary(
        string='Untaxed Amount', currency_field='currency_id',
        readonly=True, states={'draft': [('readonly', False)]})
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True, store=True)
    total_amount_company_currency = fields.Monetary(
        compute='compute_amount_company_currency', readonly=True,
        store=True, string='Total in Company Currency',
        currency_field='company_currency_id')
    untaxed_amount_company_currency = fields.Monetary(
        compute='compute_amount_company_currency', readonly=True,
        store=True, string='Untaxed Amount in Company Currency',
        currency_field='company_currency_id')
    tax_amount_company_currency = fields.Monetary(
        compute='compute_amount_company_currency', readonly=True,
        store=True, string='Tax Amount in Company Currency',
        currency_field='company_currency_id')
    # I don't use the native field 'untaxed_amount' (computed, store=True)
    has_description = fields.Boolean(compute='_compute_has_description', store=True)

    @api.depends(
        'currency_id', 'company_id', 'total_amount', 'date',
        'untaxed_amount_usability')
    def compute_amount_company_currency(self):
        for exp in self:
            date = exp.date
            if exp.currency_id and exp.company_id:
                src_currency = exp.currency_id.with_context(date=date)
                dest_currency = exp.company_id.currency_id
                total_cc = src_currency.compute(
                    exp.total_amount, dest_currency)
                untaxed_cc = src_currency.compute(
                    exp.untaxed_amount_usability, dest_currency)
                exp.total_amount_company_currency = total_cc
                exp.untaxed_amount_company_currency = untaxed_cc
                exp.tax_amount_company_currency = total_cc - untaxed_cc

    @api.multi
    @api.depends('description')
    def _compute_has_description(self):
        for rec in self:
            rec.has_description = (
                rec.description and bool(rec.description.strip()))

    @api.onchange('untaxed_amount_usability')
    def untaxed_amount_usability_change(self):
        self.tax_amount = self.total_amount - self.untaxed_amount_usability

    @api.onchange('tax_amount')
    def tax_amount_change(self):
        self.untaxed_amount_usability = self.total_amount - self.tax_amount

    @api.onchange('unit_amount', 'quantity', 'tax_ids')
    def total_amount_change(self):
        total = self.unit_amount * self.quantity
        if self.tax_ids:
            res = self.tax_ids.compute_all(
                self.unit_amount, currency=self.currency_id,
                quantity=self.quantity, product=self.product_id)
            self.untaxed_amount_usability = res['total_excluded']
            self.amount_tax = total - res['total_excluded']
        else:
            self.untaxed_amount_usability = total
            self.tax_amount = False

    @api.constrains(
        'product_id', 'payment_mode', 'tax_ids',
        'untaxed_amount_usability', 'tax_amount', 'quantity', 'unit_amount')
    def _check_expense(self):
        for exp in self:
            if exp.tax_ids:
                if len(exp.tax_ids) > 1:
                    raise ValidationError(_(
                        "The expense '%s' has several taxes. The module "
                        "'hr_expense_usability' only supports one "
                        "tax on expenses.") % exp.name)
                if not exp.tax_ids[0].price_include:
                    raise ValidationError(_(
                        "The expense '%s' has a tax that doesn't have the "
                        "property 'Included in Price'. The module "
                        "'hr_expense_usability' only accepts taxes included "
                        "in price (to avoid confusing employees).")
                        % exp.name)
            # field is hidden and default value is 'own_account', so
            # it should never happen
            if exp.payment_mode == 'company_account':
                raise ValidationError(_(
                    "Support for 'Payment By Company' is removed "
                    "by the module hr_expense_usability."))
            prec = exp.currency_id.rounding
            if float_compare(
                    exp.total_amount,
                    exp.tax_amount + exp.untaxed_amount_usability,
                    precision_rounding=prec):
                raise ValidationError(_(
                    "The expense '%s' has a total amount (%s) which is "
                    "different from the sum of the untaxed amount (%s) "
                    "and the tax amount (%s).") % (
                    exp.name,
                    exp.total_amount,
                    exp.untaxed_amount_usability,
                    exp.tax_amount))
            if (
                    not float_is_zero(
                        exp.tax_amount, precision_rounding=prec) and
                    not exp.tax_ids):
                raise ValidationError(_(
                    "The amount tax of expense '%s' is %s, "
                    "but no tax is selected.")
                    % (exp.name, exp.tax_amount))
            sign = {
                'untaxed_amount_usability': 0,
                'tax_amount': 0,
                'total_amount': 0,
                }
            for field_name in sign.iterkeys():
                sign[field_name] = float_compare(
                    exp[field_name], 0, precision_rounding=prec)
            if (
                    sign['total_amount'] < 0 and (
                        sign['untaxed_amount_usability'] > 0 or
                        sign['tax_amount'] > 0)):
                raise ValidationError(_(
                    "On the expense '%s', the total amount (%s) is "
                    "negative, so the untaxed amount (%s) and the "
                    "tax amount (%s) should be negative or null.") % (
                    exp.name,
                    exp.total_amount,
                    exp.untaxed_amount_usability,
                    exp.tax_amount))
            if (
                    sign['total_amount'] > 0 and (
                        sign['untaxed_amount_usability'] < 0 or
                        sign['tax_amount'] < 0)):
                raise ValidationError(_(
                    "On the expense '%s', the total amount (%s) is "
                    "positive, so the untaxed amount (%s) and the "
                    "tax amount (%s) should be positive or null.") % (
                    exp.name,
                    exp.total_amount,
                    exp.untaxed_amount_usability,
                    exp.tax_amount))

    def action_move_create(self):
        '''disable account.move creation per hr.expense'''
        raise UserError(_(
            "The method 'action_move_create' is blocked by the module "
            "'hr_expense_usability'"))

    @api.multi
    def _get_expense_move_lines_values(self, partner):
        self.ensure_one()
        if self.account_id:
            account = self.account_id
        else:
            account = self.product_id.product_tmpl_id. \
                _get_product_accounts()['expense']
            if not account:
                raise UserError(_(
                    "No expense account found for product '%s' nor "
                    "for it's related product category.") % (
                                    self.product_id.display_name,
                                    self.product_id.categ_id.display_name))
        return {
            'type': 'expense',
            'partner_id': partner.id,
            'account_id': account.id,
            'analytic_account_id': self.analytic_account_id.id or False,
            'amount': self.untaxed_amount_company_currency,
            'name': self.employee_id.name + ': ' +
                    self.name.split('\n')[0][:64],
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'quantity': self.quantity,
        }

    @api.multi
    def _get_expense_move_lines_tax_values(self, partner, dp):
        vals = {}
        tax_cmp = float_compare(
            self.tax_amount_company_currency, 0, precision_rounding=dp)
        if tax_cmp:
            tax = self.tax_ids[0]  # there is a constrain on this
            if tax_cmp > 0:
                tax_account_id = tax.account_id.id
            else:
                tax_account_id = tax.refund_account_id.id
            if tax.analytic:
                analytic_account_id = self.analytic_account_id.id or False
            else:
                analytic_account_id = False
            vals = {
                'type': 'tax',
                'partner_id': partner.id,
                'account_id': tax_account_id,
                'analytic_account_id': analytic_account_id,
                'amount': self.tax_amount_company_currency,
                'name': self.name.split('\n')[0][:64],
            }
        return vals


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    name = fields.Char(track_visibility='onchange')
    employee_id = fields.Many2one(track_visibility='onchange')
    responsible_id = fields.Many2one(track_visibility='onchange')
    accounting_date = fields.Date(track_visibility='onchange')
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', readonly=True, store=True)
    total_amount_company_currency = fields.Monetary(
        compute='compute_total_company_currency',
        currency_field='company_currency_id', readonly=True, store=True,
        string='Total', help="Total amount (with taxes) in company currency")
    untaxed_amount_company_currency = fields.Monetary(
        compute='compute_total_company_currency',
        currency_field='company_currency_id', readonly=True, store=True,
        string='Untaxed Amount', help="Untaxed amount in company currency")
    tax_amount_company_currency = fields.Monetary(
        compute='compute_total_company_currency',
        currency_field='company_currency_id', readonly=True, store=True,
        string='Tax Amount', help="Tax amount in company currency")
    account_move_id = fields.Many2one(
        ondelete='restrict')

    @api.depends(
        'expense_line_ids.total_amount_company_currency',
        'expense_line_ids.untaxed_amount_company_currency')
    def compute_total_company_currency(self):
        for sheet in self:
            total = 0.0
            untaxed = 0.0
            for line in sheet.expense_line_ids:
                total += line.total_amount_company_currency
                untaxed += line.untaxed_amount_company_currency
            sheet.total_amount_company_currency = total
            sheet.untaxed_amount_company_currency = untaxed
            sheet.tax_amount_company_currency = total - untaxed

    @api.multi
    def _compute_attachment_number(self):
        AttachmentObj = self.env['ir.attachment']
        for rec in self:
            sheet_attachment_count = AttachmentObj.search_count([
                ('res_model', '=', self._name),
                ('res_id', '=', rec.id)])
            rec.attachment_number = (
                sum(self.expense_line_ids.mapped('attachment_number')) +
                sheet_attachment_count)

    @api.multi
    def action_get_attachment_view(self):
        self.ensure_one()
        res = super(HrExpenseSheet, self).action_get_attachment_view()
        res['domain'] = [
            '|',
            '&',
            ('res_model', '=', 'hr.expense'),
            ('res_id', 'in', self.expense_line_ids.ids),
            '&',
            ('res_model', '=', 'hr.expense.sheet'),
            ('res_id', '=', self.id),
        ]
        return res

    @api.one
    @api.constrains('expense_line_ids')
    def _check_amounts(self):
        '''Remove the constraint 'You cannot have a positive and negative
        amounts on the same expense report.' '''
        return True

    def _prepare_move(self):
        self.ensure_one()
        if not self.journal_id:
            raise UserError(_(
                "No journal selected for expense report %s.")
                % self.display_name)
        date = self.accounting_date or fields.Date.context_today(self)
        vals = {
            'name': '/',
            'journal_id': self.journal_id.id,
            'date': date,
            'ref': self.number,
            'company_id': self.company_id.id,
            'line_ids': [],
            }
        return vals

    def _prepare_payable_move_line(self, total_company_currency):
        self.ensure_one()
        debit = credit = False
        prec = self.company_id.currency_id.rounding
        if float_compare(
                total_company_currency, 0, precision_rounding=prec) > 0:
            credit = total_company_currency
        else:
            debit = total_company_currency * -1
        partner = self.employee_id._get_accounting_partner_from_employee()
        # by default date_maturity = move date
        vals = {
            'account_id': partner.property_account_payable_id.id,
            'partner_id': partner.id,
            'name': self.name[:64],
            'credit': credit,
            'debit': debit,
            }
        return vals

    @api.model
    def _get_group_key(self, mline, group, i):
        if group:
            key = [
                mline['type'],
                mline['account_id'],
                mline['analytic_account_id'],
                False]
        else:
            key = [False, False, False, i]
        return key

    @api.model
    def _prepare_expense_move_lines_values(self, gmlines, dp):
        credit = debit = False
        cmp_amount = float_compare(
            gmlines['amount'], 0, precision_rounding=dp)
        if cmp_amount > 0:
            debit = gmlines['amount']
        elif cmp_amount < 0:
            credit = gmlines['amount'] * -1
        else:
            return False
        return {
            'partner_id': gmlines['partner_id'],
            'account_id': gmlines['account_id'],
            'analytic_account_id': gmlines['analytic_account_id'],
            'product_id': gmlines.get('product_id', False),
            'product_uom_id': gmlines.get('product_uom_id', False),
            'quantity': gmlines.get('quantity', 1),
            'name': gmlines['name'],
            'debit': debit,
            'credit': credit,
        }

    def _prepare_expense_move_lines(self):
        self.ensure_one()
        mlines = []
        partner = self.employee_id._get_accounting_partner_from_employee()
        prec = self.company_id.currency_id.rounding
        for exp in self.expense_line_ids:
            # Expense
            vals = exp._get_expense_move_lines_values(partner)
            mlines.append(vals)
            # TAX
            tax_line_values = exp._get_expense_move_lines_tax_values(
                partner, prec)
            if tax_line_values:
                mlines.append(tax_line_values)
        # grouping
        group_mlines = {}
        group = self.journal_id.group_invoice_lines
        i = 0
        for mline in mlines:
            i += 1
            key = tuple(self._get_group_key(mline, group, i))
            if key in group_mlines:
                group_mlines[key]['amount'] += mline['amount']
                group_mlines[key]['name'] = self.name[:64]
                group_mlines[key]['quantity'] += mline['quantity']
                if 'product_id' in group_mlines[key] and \
                        group_mlines[key]['product_id'] != \
                        mline['product_id']:
                    del group_mlines[key]['product_id']
                if 'product_uom_id' in group_mlines[key] and \
                        group_mlines[key]['product_uom_id'] != \
                        mline['product_uom_id']:
                    del group_mlines[key]['product_uom_id']
            else:
                group_mlines[key] = mline
        res_mlines = []
        total_cc = 0.0
        for gmlines in group_mlines.itervalues():
            total_cc += gmlines['amount']
            vals = self._prepare_expense_move_lines_values(gmlines, prec)
            if vals:
                res_mlines.append((0, 0, vals))
        return res_mlines, total_cc

    def action_sheet_move_create(self):
        for sheet in self:
            if sheet.state != 'approve':
                raise UserError(_(
                    "It is possible to generate accounting entries only "
                    "for approved expense reports. The expense report %s "
                    "is in state '%s'.") % (sheet.number, sheet.state))
            if float_is_zero(
                    sheet.total_amount,
                    precision_rounding=sheet.company_id.currency_id.rounding):
                raise UserError(_(
                    "The expense report %s has a total amount of 0.")
                    % sheet.number)

            vals = sheet._prepare_move()
            exp_mlvals_list, total_cc = self._prepare_expense_move_lines()
            vals['line_ids'] += exp_mlvals_list
            pay_mlvals = sheet._prepare_payable_move_line(total_cc)
            vals['line_ids'].append((0, 0, pay_mlvals))
            move = self.env['account.move'].create(vals)
            sheet.write(sheet._prepare_sheet_write_move_create(move))

    def _prepare_sheet_write_move_create(self, move):
        self.ensure_one()
        vals = {
            'state': 'post',
            'account_move_id': move.id,
        }
        if not self.accounting_date:
            vals['accounting_date'] = move.date
        return vals

    # TODO: for multi-company with expenses envir., we would need a field
    # 'default_expense_journal' on company (otherwise, it takes the
    # first purchase journal, which is probably not the good one
