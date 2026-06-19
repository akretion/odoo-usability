# Copyright Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class CommissionResult(models.Model):
    _name = 'commission.result'
    _description = "Commission Result"
    _order = 'date_start desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one(
        'res.partner', string='Salesman/Agent', required=True, ondelete='restrict',
        readonly=True, tracking=True)
    profile_id = fields.Many2one(
        'commission.profile', string='Commission Profile', readonly=True, tracking=True)
    assignment_id = fields.Many2one(
        'commission.profile.assignment', string="Commission Profile Assignment", readonly=True)
    assign_type = fields.Selection('_assign_type_selection', readonly=True, tracking=True)
    company_id = fields.Many2one(
        'res.company', string='Company', ondelete='cascade',
        required=True, readonly=True, default=lambda self: self.env.company, tracking=True)
    company_currency_id = fields.Many2one(
        related='company_id.currency_id', string='Company Currency', store=True)
    date_range_id = fields.Many2one(
        'date.range', required=True, string='Period', readonly=True, tracking=True)
    date_start = fields.Date(related='date_range_id.date_start', store=True)
    date_end = fields.Date(related='date_range_id.date_end', store=True)
    line_ids = fields.One2many(
        'account.move.line', 'commission_result_id', string='Commission Lines',
        states={'done': [('readonly', True)]})
    amount_total = fields.Monetary(
        string='Commission Total', currency_field='company_currency_id',
        compute='_compute_totals', store=True, tracking=True)
    base_total = fields.Monetary(
        string="Commission Base Total", currency_field='company_currency_id',
        compute='_compute_totals', store=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ], default='draft', tracking=True)
    # TODO copy amount to another field
    # help='This is the total amount at the date of the computation of the commission')

    @api.model
    def _assign_type_selection(self):
        return self.env['commission.profile.assignment']._assign_type_selection()

    @api.depends('line_ids.commission_amount', 'line_ids.commission_base')
    def _compute_totals(self):
        rg_res = self.env['account.move.line'].read_group([('commission_result_id', 'in', self.ids)], ['commission_result_id', 'commission_amount:sum', 'commission_base:sum'], ['commission_result_id'])
        mapped_data = dict([(x['commission_result_id'][0], {'amount': x['commission_amount'], 'base': x['commission_base']}) for x in rg_res])
        for rec in self:
            rec.amount_total = mapped_data.get(rec.id, {}).get('amount')
            rec.base_total = mapped_data.get(rec.id, {}).get('base')

    def unlink(self):
        for result in self:
            if result.state == 'done':
                raise UserError(_(
                    "You cannot delete commission result %s because it is in done state.") % result.display_name)
        return super().unlink()

    def draft2done(self):
        self.filtered(lambda x: x.state == 'draft').write({'state': 'done'})

    def backtodraft(self):
        self.write({'state': 'draft'})

    def name_get(self):
        res = []
        for result in self:
            name = '%s (%s)' % (result.partner_id.name, result.date_range_id.name)
            res.append((result.id, name))
        return res

    _sql_constraints = [(
        'salesman_period_company_unique',
        'unique(company_id, partner_id, date_range_id)',
        'A commission result already exists for this salesman/agent for the same period.')]

    def _prepare_xlsx_lines(self):
        self.ensure_one()
        return self.line_ids.sorted(key=lambda x: x.move_id.invoice_date)
