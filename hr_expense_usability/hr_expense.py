# -*- coding: utf-8 -*-
# © 2014-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
import odoo.addons.decimal_precision as dp


# I had to choose between several ideas when I developped this module :
# 1) constraint on product_id in expense line
# Idea : we put a constraint on the field product_id of the expense line
# and, if it's a private_car_expense_ok=True product but it's not the private
# car expense product of the employee, we block
# Drawback : not convenient for the employee because he has to select the
# right private car expense product by himself

# 2) single product, dedicated object for prices
# Idea : we create only one "private car expense" product, and we
# create a new object to store the price depending on the CV, etc...
# Drawback : need to create a new object
# => that's what is implemented in this module

# 3) single generic "My private car" product selectable by the user ;
# several specific private car products NOT selectable by the user
# Idea : When the user selects the generic "My private car" product,
# it is automatically replaced by the specific one via the on_change
# Drawback : decimal precision 'Product Price' on standard_price of product
# (but we need 3)

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


class PrivateCarKmPrice(models.Model):
    _name = 'private.car.km.price'
    _description = 'Private Car Kilometer Price'
    _order = 'name'

    name = fields.Char(required=True)
    unit_amount = fields.Float(
        string='Price per KM', digits=dp.get_precision('Expense Unit Price'),
        help='Price per kilometer in company currency.')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'private.car.km.price'))
    active = fields.Boolean(default=True)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def compute_private_car_total_km_this_year(self):
        res = {}
        private_car_product_id = self.env.ref(
            'hr_expense_usability.generic_private_car_expense').id
        today = fields.Date.context_today(self)
        today_dt = fields.Date.from_string(today)
        self._cr.execute(
            """
            SELECT el.employee_id, sum(el.quantity)
            FROM hr_expense el
            WHERE el.state NOT IN ('draft', 'cancel')
            AND el.employee_id IN %s
            AND el.product_id=%s
            AND EXTRACT(year FROM el.date) = %s
            GROUP BY el.employee_id
            """,
            (tuple(self.ids), private_car_product_id, today_dt.year))
        for line in self._cr.dictfetchall():
            res[line['employee_id']] = line['sum']
        for empl in self:
            empl.private_car_total_km_this_year = res.get(empl.id) or 0.0

    private_car_plate = fields.Char(
        'Private Car Plate', size=32, copy=False, track_visibility='onchange',
        help="This field will be copied on the expenses of this employee.")
    private_car_km_price_id = fields.Many2one(
        'private.car.km.price', string='Private Car Price', copy=False,
        ondelete='restrict', track_visibility='onchange',
        help="This field will be copied on the expenses of this employee.")
    private_car_total_km_this_year = fields.Float(
        compute='compute_private_car_total_km_this_year',
        string="Total KM with Private Car This Year", readonly=True,
        help="Number of kilometers (KM) with private car for this "
        "employee in expenses in Approved, Waiting Payment or Paid "
        "state in the current civil year. This is usefull to check or "
        "estimate if the Private Car Product selected for this "
        "employee is compatible with the number of kilometers "
        "reimbursed to this employee during the civil year.")

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
    private_car_plate = fields.Char(
        string='Private Car Plate', size=32, track_visibility='onchange',
        readonly=True, states={'draft': [('readonly', False)]})
    private_car_km_price_id = fields.Many2one(
        'private.car.km.price', string='Private Car Price', copy=False,
        ondelete='restrict', track_visibility='onchange',
        help="This field will be copied on the expenses of this employee.")
    # only for field visibility
    private_car_expense = fields.Boolean()
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

    @api.onchange('product_id')
    def _onchange_product_id(self):
        private_car_product = self.env.ref(
            'hr_expense_usability.generic_private_car_expense')
        if (
                self.product_id and
                self.product_id == private_car_product and
                self.employee_id):
            if not self.employee_id.private_car_km_price_id:
                raise UserError(_(
                    "Missing Private Car Km Price on the configuration of "
                    "the employee '%s'.") % self.employee_id.display_name)
            if not self.employee_id.private_car_plate:
                raise UserError(_(
                    "Missing Private Car Plate on the configuration of "
                    "the employee '%s'.") % self.employee_id.display_name)
            self.private_car_expense = True
            self.currency_id = self.company_id.currency_id
            self.private_car_plate = self.employee_id.private_car_plate
            self.private_car_km_price_id =\
                self.employee_id.private_car_km_price_id
        else:
            self.private_car_expense = False
            self.private_car_plate = False
            self.private_car_km_price_id = False
        return super(HrExpense, self)._onchange_product_id()

    @api.onchange('private_car_km_price_id')
    def _onchange_private_car_km_price_id(self):
        if self.private_car_km_price_id and self.employee_id:
            self.unit_amount =\
                self.employee_id.private_car_km_price_id.unit_amount

    @api.onchange('unit_amount')
    def _onchange_unit_amount(self):
        res = {}
        if self.private_car_expense:
            original_unit_amount = self.private_car_km_price_id.unit_amount
            prec = self.env['decimal.precision'].precision_get(
                'Expense Unit Price')
            if float_compare(
                    original_unit_amount, self.unit_amount,
                    precision_digits=prec):
                if self.env.user.has_group('account.group_account_manager'):
                    res['warning'] = {
                        'title': _('Warning - Private Car Expense'),
                        'message': _(
                            "You should not change the unit price "
                            "for private car expenses. You should change "
                            "the Private Car Product or update the Cost "
                            "Price of the selected Private Car Product "
                            "and re-create the Expense.\n\nBut, as "
                            "you are in the group 'Account Manager', we "
                            "suppose that you know what you are doing, "
                            "so the original unit amount (%s) is not "
                            "restored.") % original_unit_amount,
                        }
                else:
                    res['warning'] = {
                        'title': _('Warning - Private Car Expense'),
                        'message': _(
                            "You should not change the unit price "
                            "for private car expenses. The original unit "
                            "amount has been restored.\n\nOnly users in "
                            "the 'Account Manager' group are allowed to "
                            "change the unit amount for private car "
                            "expenses manually.")}
                    res['value'] = {'unit_amount': original_unit_amount}
        return res

    @api.constrains(
        'product_id', 'private_car_plate', 'payment_mode', 'tax_ids',
        'untaxed_amount_usability', 'tax_amount', 'quantity', 'unit_amount')
    def _check_expense(self):
        generic_private_car_product = self.env.ref(
            'hr_expense_usability.generic_private_car_expense')
        for exp in self:
            if exp.product_id == generic_private_car_product:
                if not exp.private_car_plate:
                    raise ValidationError(_(
                        "Missing 'Private Car Plate' on the "
                        "expense '%s' of employee '%s'.")
                        % (exp.name, exp.employee_id.display_name))
                if not exp.private_car_km_price_id:
                    raise ValidationError(_(
                        "Missing 'Private Car Km Price' on the "
                        "expense '%s'.") % exp.name)
                if exp.currency_id != exp.company_id.currency_id:
                    raise ValidationError(_(
                        "The expense '%s' is a private car expense, "
                        "so the currency of this expense (%s) should "
                        "be the currency of the company (%s).") % (
                        exp.name,
                        exp.currency_id.name,
                        exp.company_id.currency_id.name))
                if exp.tax_ids:
                    raise ValidationError(_(
                        "The expense '%s' is a private car expense "
                        "so it shouldn't have taxes.")
                        % exp.name)
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

    def _prepare_expense_move_lines(self):
        self.ensure_one()
        mlines = []
        partner = self.employee_id._get_accounting_partner_from_employee()
        prec = self.company_id.currency_id.rounding
        for exp in self.expense_line_ids:
            # Expense
            if exp.account_id:
                account = exp.account_id
            else:
                account = exp.product_id.product_tmpl_id.\
                    _get_product_accounts()['expense']
                if not account:
                    raise UserError(_(
                        "No expense account found for product '%s' nor "
                        "for it's related product category.") % (
                        exp.product_id.display_name,
                        exp.product_id.categ_id.display_name))
            mlines.append({
                'type': 'expense',
                'partner_id': partner.id,
                'account_id': account.id,
                'analytic_account_id': exp.analytic_account_id.id or False,
                'amount': exp.untaxed_amount_company_currency,
                'name': exp.name.split('\n')[0][:64],
                })
            # TAX
            tax_cmp = float_compare(
                exp.tax_amount_company_currency, 0, precision_rounding=prec)
            if tax_cmp:
                tax = exp.tax_ids[0]  # there is a constrain on this
                if tax_cmp > 0:
                    tax_account_id = tax.account_id.id
                else:
                    tax_account_id = tax.refund_account_id.id
                if tax.analytic:
                    analytic_account_id = exp.analytic_account_id.id or False
                else:
                    analytic_account_id = False
                mlines.append({
                    'type': 'tax',
                    'partner_id': partner.id,
                    'account_id': tax_account_id,
                    'analytic_account_id': analytic_account_id,
                    'amount': exp.tax_amount_company_currency,
                    'name': exp.name.split('\n')[0][:64],
                    })
        # grouping
        group_mlines = {}
        group = self.journal_id.group_invoice_lines
        i = 0
        for mline in mlines:
            i += 1
            if group:
                key = (
                    mline['type'],
                    mline['account_id'],
                    mline['analytic_account_id'],
                    False)
            else:
                key = (False, False, False, i)
            if key in group_mlines:
                group_mlines[key]['amount'] += mline['amount']
                group_mlines[key]['name'] = self.name[:64]
            else:
                group_mlines[key] = mline
        res_mlines = []
        total_cc = 0.0
        for gmlines in group_mlines.itervalues():
            total_cc += gmlines['amount']
            credit = debit = False
            cmp_amount = float_compare(
                gmlines['amount'], 0, precision_rounding=prec)
            if cmp_amount > 0:
                debit = gmlines['amount']
            elif cmp_amount < 0:
                credit = gmlines['amount'] * -1
            else:
                continue
            res_mlines.append((0, 0, {
                'partner_id': gmlines['partner_id'],
                'account_id': gmlines['account_id'],
                'analytic_account_id': gmlines['analytic_account_id'],
                'name': gmlines['name'],
                'debit': debit,
                'credit': credit,
                }))
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
