# -*- coding: utf-8 -*-
# Copyright Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class CommissionProfile(models.Model):
    _name = 'commission.profile'
    _description = 'Commission Profile'

    name = fields.Char(string='Name of the Profile', required=True)
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        required=True,
        default=lambda self: self.env['res.company']._company_default_get())
    line_ids = fields.One2many(
        'commission.rule', 'profile_id', string='Commission Rules')
    trigger_type = fields.Selection([
        ('invoice', 'Invoicing'),
        ('payment', 'Payment'),
        ], default='invoice', string='Trigger', required=True)


class CommissionRule(models.Model):
    _name = 'commission.rule'
    _description = 'Commission Rule'
    _order = 'profile_id, applied_on'

    partner_ids = fields.Many2many(
        'res.partner', string='Customers',
        domain=[('parent_id', '=', False), ('customer', '=', True)])
    product_categ_ids = fields.Many2many(
        'product.category', string="Product Categories",
        domain=[('type', '=', 'normal')])
    product_ids = fields.Many2many('product.product', string='Products')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    profile_id = fields.Many2one(
        'commission.profile', string='Profile', ondelete='cascade')
    company_id = fields.Many2one(
        related='profile_id.company_id', store=True, readonly=True)
    rate = fields.Float(
        'Commission Rate', digits=dp.get_precision('Commission Rate'),
        copy=False)
    applied_on = fields.Selection([
        ('0_customer_product', 'Products and Customers'),
        ('1_customer_product_category', "Product Categories and Customers"),
        ('2_product', "Products"),
        ('3_product_category', "Product Categories"),
        ('4_global', u'Global')],
        string='Apply On', default='4_global', required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def load_all_rules(self):
        rules = self.search_read()
        res = {}  # key = profile, value = [rule1 recordset, rule2]
        for rule in rules:
            if rule['profile_id']:
                if rule['profile_id'][0] not in res:
                    res[rule['profile_id'][0]] = [rule]
                else:
                    res[rule['profile_id'][0]].append(rule)
        return res

    _sql_constraints = [(
        'rate_positive',
        'CHECK(rate >= 0)',
        'Rate must be positive !')]


class CommissionResult(models.Model):
    _name = 'commission.result'
    _description = "Commission Result"
    _order = 'date_start desc'

    user_id = fields.Many2one(
        'res.users', 'Salesman', required=True, ondelete='restrict',
        readonly=True)
    profile_id = fields.Many2one(
        'commission.profile', string='Commission Profile',
        readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        required=True, readonly=True,
        default=lambda self: self.env['res.company']._company_default_get())
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', string='Company Currency',
        readonly=True, store=True)
    date_range_id = fields.Many2one(
        'date.range', required=True, string='Period', readonly=True)
    date_start = fields.Date(
        related='date_range_id.date_start', readonly=True, store=True)
    date_end = fields.Date(
        related='date_range_id.date_end', readonly=True, store=True)
    line_ids = fields.One2many(
        'account.invoice.line', 'commission_result_id', 'Commission Lines',
        readonly=True)
    amount_total = fields.Monetary(
        string='Commission Total', currency_field='company_currency_id',
        help='This is the total amount at the date of the computation of the commission',
        readonly=True)

    def name_get(self):
        res = []
        for result in self:
            name = '%s (%s)' % (result.user_id.name, result.date_range_id.name)
            res.append((result.id, name))
        return res

    _sql_constraints = [(
        'salesman_period_company_unique',
        'unique(company_id, user_id, date_range_id)',
        'A commission result already exists for this salesman for '
        'the same period')]
