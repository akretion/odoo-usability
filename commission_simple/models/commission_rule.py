# Copyright Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models, api, _


class CommissionRule(models.Model):
    _name = 'commission.rule'
    _description = 'Commission Rule'
    _order = 'profile_id, applied_on, rate desc'

    partner_ids = fields.Many2many(
        'res.partner', string='Customers', domain=[('parent_id', '=', False)])
    product_categ_ids = fields.Many2many(
        'product.category', string="Product Categories")
    product_ids = fields.Many2many('product.product', string='Products')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    profile_id = fields.Many2one(
        'commission.profile', string='Profile', ondelete='cascade')
    company_id = fields.Many2one(related='profile_id.company_id', store=True)
    rate = fields.Float('Commission Rate', digits="Commission Rate", copy=False)
    base = fields.Selection([
        ('invoiced', 'Invoiced Amount'),
        ('margin', 'Margin'),
        ], default='invoiced', required=True, string="Commission Base")
    applied_on = fields.Selection([
        ('0_customer_product', 'Products and Customers'),
        ('1_customer_product_category', "Product Categories and Customers"),
        ('2_product', "Products"),
        ('3_product_category', "Product Categories"),
        ('4_global', 'Global')],
        string='Apply On', default='4_global', required=True)
    active = fields.Boolean(string='Active', default=True)
    apply_description = fields.Html(compute='_compute_apply_description', string="Match Criteria")

    _sql_constraints = [(
        'rate_positive',
        'CHECK(rate >= 0)',
        'Rate must be positive !')]

    def _compute_apply_description(self):
        customer_label = "<strong>" + _("Customers:") + "</strong>"
        product_label = "<strong>" + _("Products:") + "</strong>"
        product_categ_label = "<strong>" + _("Product Categories:") + "</strong>"
        and_label = "<strong>" + _('AND') + "</strong>"
        for rule in self:
            desc = False
            if rule.applied_on == '0_customer_product':
                desc = f"{customer_label} {', '.join([part.ref or part.name for part in rule.partner_ids])} {and_label} {product_label} {', '.join([pp.default_code or pp.name for pp in rule.product_ids])}"
            elif rule.applied_on == '1_customer_product_category':
                desc = f"{customer_label} {', '.join([part.ref or part.name for part in rule.partner_ids])} {and_label} {product_categ_label} {', '.join([categ.display_name for categ in rule.product_categ_ids])}"
            elif rule.applied_on == '2_product':
                desc = f"{product_label} {', '.join([pp.default_code or pp.name for pp in rule.product_ids])}"
            elif rule.applied_on == '3_product_category':
                desc = f"{product_categ_label} {', '.join([categ.display_name for categ in rule.product_categ_ids])}"
            elif rule.applied_on == '4_global':
                desc = _('Global')
            rule.apply_description = desc

    @api.model
    def load_all_rules(self):
        rules = self.search_read([('profile_id', '!=', False)])
        res = {}  # key = profile, value = [rule1 recordset, rule2]
        for rule in rules:
            if rule['profile_id'][0] not in res:
                res[rule['profile_id'][0]] = [rule]
            else:
                res[rule['profile_id'][0]].append(rule)
        return res
