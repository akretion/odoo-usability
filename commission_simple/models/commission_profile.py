# Copyright Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class CommissionProfile(models.Model):
    _name = 'commission.profile'
    _description = 'Commission Profile'
    _order = 'sequence, id'

    name = fields.Char(string='Name of the Profile', required=True)
    active = fields.Boolean(string='Active', default=True)
    sequence = fields.Integer()
    company_id = fields.Many2one(
        'res.company', string='Company', ondelete='cascade',
        required=False, default=lambda self: self.env.company)
    assign_ids = fields.One2many(
        'commission.profile.assignment', 'profile_id', string="Assignments")
    rule_ids = fields.One2many(
        'commission.rule', 'profile_id', string='Commission Rules')
    trigger_type = fields.Selection([
        ('invoice', 'Invoiced'),
        ('paid', 'Paid'),
        ('in_payment', 'In Payment and Paid'),
        ], default='paid', string='Trigger', required=True)
    date_range_type_id = fields.Many2one(
        'date.range.type', string='Commission Periodicity', ondelete='restrict',
        domain="[('company_id', 'in', (False, company_id))]")


class CommissionProfileAssignment(models.Model):
    _name = "commission.profile.assignment"
    _description = "Commission Profile Assignment"

    profile_id = fields.Many2one('commission.profile', ondelete='cascade')
    company_id = fields.Many2one(
        'res.company', string='Company', ondelete='cascade',
        required=True, default=lambda self: self.env.company)
    assign_type = fields.Selection(
        '_assign_type_selection', default='user', required=True, string="Type")
    user_id = fields.Many2one(
        'res.users', compute="_compute_user_id", store=True, precompute=True, readonly=False,
        ondelete="restrict", string="Salesman",
        )

    _sql_constraints = [
        (
            'company_user_uniq',
            'unique(user_id, company_id)',
            'This salesman already has an assignment in this company.')]

    @api.model
    def _assign_type_selection(self):
        return [('user', _('Salesman'))]

    @api.constrains('assign_type', 'user_id')
    def _check_user(self):
        for assignment in self:
            if assignment.assign_type == 'user' and not assignment.user_id:
                raise ValidationError(_("A salesman must be selected when the assignment type is 'Salesman'."))

    @api.depends('assign_type')
    def _compute_user_id(self):
        for assign in self:
            if assign.assign_type != 'user':
                assign.user_id = False

    def _get_partner(self):
        self.ensure_one()
        if self.assign_type == 'user':
            return self.user_id.partner_id
        return False

    def _prepare_move_line_domain(self, date_range):
        self.ensure_one()
        domain = [
            ('display_type', '=', 'product'),
            ('move_id.move_type', 'in', ('out_invoice', 'out_refund')),
            ('date', '<=', date_range.date_end),
            ('company_id', '=', self.company_id.id),
            ('commission_result_id', '=', False),
            ('parent_state', '=', 'posted'),
            ]
        if self.assign_type == 'user':
            domain.append(('move_id.invoice_user_id', '=', self.user_id.id))
        # TODO : for trigger 'paid' and 'in_payment', we would need to filter
        # out the invoices paid after the end date of the commission period
        if self.profile_id.trigger_type == 'paid':
            domain.append(('move_id.payment_state', 'in', ('paid', 'reversed')))
        elif self.profile_id.trigger_type == 'in_payment':
            domain.append(('move_id.payment_state', 'in', ('in_payment', 'paid', 'reversed')))
        elif self.profile_id.trigger_type == 'invoice':
            domain.append(('date', '>=', date_range.date_start))
        return domain

    def _prepare_commission_result(self, date_range):
        vals = {
            'partner_id': self._get_partner().id,
            'profile_id': self.profile_id.id,
            'date_range_id': date_range.id,
            'assign_type': self.assign_type,
            'assignment_id': self.id,
            'company_id': self.company_id.id,
            }
        return vals

    def _generate_commission_result(self, date_range, rules):
        self.ensure_one()
        ilines = self.env['account.move.line'].search(
            self._prepare_move_line_domain(date_range), order='date, move_id, sequence, id')
        profile = self.profile_id
        ilines2write = {}
        for iline in ilines:
            rule = iline._match_commission_rule(rules[profile.id])
            if rule:
                lvals = iline._prepare_commission_data(rule)
                if lvals:
                    ilines2write[iline] = lvals
        if ilines2write:
            com_result = self.env['commission.result'].create(self._prepare_commission_result(date_range))
            for iline, vals in ilines2write.items():
                iline.write(dict(vals, commission_result_id=com_result.id))
            return com_result
        else:
            return False
