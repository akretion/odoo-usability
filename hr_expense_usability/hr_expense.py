# -*- coding: utf-8 -*-
# © 2014-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


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

# 3) single generic "My private car" product selectable by the user ;
# several specific private car products NOT selectable by the user
# Idea : When the user selects the generic "My private car" product,
# it is automatically replaced by the specific one via the on_change
# Drawback : none ? :)
# => that's what is implemented in this module


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    private_car_expense_ok = fields.Boolean(
        string='Private Car Expense', track_visibility='onchange')

    @api.onchange('private_car_expense_ok')
    def onchange_private_car_expense_ok(self):
        if self.private_car_expense_ok:
            km_uom = self.env.ref('product.product_uom_km')
            self.type = 'service'
            self.list_price = 0.0
            self.can_be_expensed = False
            self.sale_ok = False
            self.purchase_ok = False
            self.uom_id = km_uom.id
            self.po_uom_id = km_uom.id
            self.taxes_id = False
            self.supplier_taxes_id = False

    @api.constrains(
        'private_car_expense_ok', 'can_be_expensed', 'uom_id',
        'standard_price')
    def _check_private_car_expense(self):
        for product in self:
            if product.private_car_expense_ok:
                if product.can_be_expensed:
                    raise ValidationError(_(
                        "The product '%s' cannot have both the properties "
                        "'Can be Expensed' and 'Private Car Expense'.")
                        % product.display_name)
                km_uom = self.env.ref('product.product_uom_km')
                if product.uom_id != km_uom:
                    raise ValidationError(_(
                        "The product '%s' is a Private Car Expense, so "
                        "it's unit of measure must be kilometers (KM).")
                        % product.display_name)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def compute_private_car_total_km_this_year(self):
        print "compute_private_car_total_km_this_year self=", self
        res = {}
        private_car_products = self.env['product.product'].search(
            [('private_car_expense_ok', '=', True)])
        today = fields.Date.context_today(self)
        today_dt = fields.Date.from_string(today)
        self._cr.execute(
            """
            SELECT el.employee_id, sum(el.quantity)
            FROM hr_expense el
            WHERE el.state NOT IN ('draft', 'cancel')
            AND el.employee_id IN %s
            AND el.product_id IN %s
            AND EXTRACT(year FROM el.date) = %s
            GROUP BY el.employee_id
            """,
            (tuple(self.ids), tuple(private_car_products.ids), today_dt.year))
        for line in self._cr.dictfetchall():
            res[line['employee_id']] = line['sum']
        for empl in self:
            empl.private_car_total_km_this_year = res.get(empl.id) or 0.0

    private_car_plate = fields.Char(
        'Private Car Plate', size=32, copy=False, track_visibility='onchange',
        help="This field will be copied on the expenses of this employee.")
    private_car_product_id = fields.Many2one(
        'product.product', string='Private Car Product', copy=False,
        domain=[('private_car_expense_ok', '=', True)],
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


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    private_car_plate = fields.Char(
        string='Private Car Plate', size=32, readonly=True,
        track_visibility='onchange',
        states={'draft': [('readonly', False)]})
    private_car_expense = fields.Boolean(
        related='product_id.private_car_expense_ok', readonly=True, store=True)

    # as private_car_plate id readonly, we have to inherit create() to set it

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if (
                self.product_id and self.product_id == self.env.ref(
                    'hr_expense_usability.generic_private_car_expense')):
            if not self.employee_id.private_car_product_id:
                raise UserError(_(
                    "Missing Private Car Product on the configuration of "
                    "the employee '%s'.") % self.employee_id.display_name)
            if not self.employee_id.private_car_plate:
                raise UserError(_(
                    "Missing Private Car Plate on the configuration of "
                    "the employee '%s'.") % self.employee_id.display_name)
            self.product_id = self.employee_id.private_car_product_id
            self.private_car_plate = self.employee_id.private_car_plate
        return super(HrExpense, self)._onchange_product_id()

    @api.onchange('unit_amount')
    def _onchange_unit_amount(self):
        res = {}
        if self.product_id.private_car_expense_ok:
            original_unit_amount = self.product_id.price_compute(
                'standard_price')[self.product_id.id]
            prec = self.env['decimal.precision'].precision_get('Product Price')
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

    @api.constrains('product_id')
    def _check_private_car(self):
        generic_private_car_product = self.env.ref(
            'hr_expense_usability.generic_private_car_expense')
        for exp in self:
            if exp.product_id == generic_private_car_product:
                raise ValidationError(_(
                    "You are trying to save the expense '%s' "
                    "with the generic product '%s': it is not possible, "
                    "this product should have been automatically replaced "
                    "by the specific private car product configured for "
                    "the employee '%s'.") % (
                        exp.name,
                        generic_private_car_product.name,
                        exp.employee_id.display_name))
            if (
                    exp.product_id.private_car_expense_ok and
                    not exp.private_car_plate):
                raise ValidationError(_(
                    "Missing 'Private Car Plate' on the "
                    "expense '%s' of employee '%s'.")
                    % (exp.name, exp.employee_id.display_name))
