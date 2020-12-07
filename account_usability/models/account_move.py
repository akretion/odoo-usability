# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.tools.misc import formatLang
from odoo.tools.misc import format_date
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class AccountMove(models.Model):
    _inherit = 'account.move'

    default_move_line_name = fields.Char(
        string='Default Label', states={'posted': [('readonly', True)]})
    # By default, we can still modify "ref" when account move is posted
    # which seems a bit lazy for me...
    ref = fields.Char(states={'posted': [('readonly', True)]})
    date = fields.Date(tracking=True)
    invoice_date_due = fields.Date(tracking=True)
    invoice_payment_term_id = fields.Many2one(tracking=True)
    journal_id = fields.Many2one(tracking=True)
    partner_bank_id = fields.Many2one(tracking=True)
    fiscal_position_id = fields.Many2one(tracking=True)
    amount_total = fields.Monetary(tracking=True)
    # for invoice report
    has_discount = fields.Boolean(
        compute='_compute_has_discount', readonly=True)
    # has_attachment is useful for those who use attachment to archive
    # supplier invoices. It allows them to find supplier invoices
    # that don't have any attachment
    has_attachment = fields.Boolean(
        compute='_compute_has_attachment',
        search='_search_has_attachment', readonly=True)
    sale_dates = fields.Char(
        compute="_compute_sales_dates", readonly=True,
        help="This information appears on invoice qweb report "
             "(you may use it for your own report)")

    def _compute_has_discount(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        for inv in self:
            has_discount = False
            for line in inv.invoice_line_ids:
                if not line.display_type and not float_is_zero(line.discount, precision_digits=prec):
                    has_discount = True
                    break
            inv.has_discount = has_discount

    def _compute_has_attachment(self):
        iao = self.env['ir.attachment']
        for move in self:
            if iao.search([
                    ('res_model', '=', 'account.move'),
                    ('res_id', '=', move.id),
                    ('type', '=', 'binary'),
                    ('company_id', '=', move.company_id.id)], limit=1):
                inv.has_attachment = True
            else:
                inv.has_attachment = False

    def _search_has_attachment(self, operator, value):
        att_inv_ids = {}
        if operator == '=':
            search_res = self.env['ir.attachment'].search_read([
                ('res_model', '=', 'account.move'),
                ('type', '=', 'binary'),
                ('res_id', '!=', False)], ['res_id'])
            for att in search_res:
                att_inv_ids[att['res_id']] = True
        res = [('id', value and 'in' or 'not in', list(att_inv_ids))]
        return res

    # when you have an invoice created from a lot of sale orders, the 'name'
    # field is very large, which makes the name_get() of that invoice very big
    # which screws-up the form view of that invoice because of the link at the
    # top of the screen
    # That's why we have to cut the name_get() when it's too long
    def name_get(self):
        old_res = super().name_get()
        res = []
        for old_re in old_res:
            name = old_re[1]
            if name and len(name) > 100:
                # nice cut
                name = '%s ...' % ', '.join(name.split(', ')[:3])
                # if not enough, hard cut
                if len(name) > 120:
                    name = '%s ...' % old_re[1][:120]
            res.append((old_re[0], name))
        return res

    # I really hate to see a "/" in the 'name' field of the account.move.line
    # generated from customer invoices linked to the partners' account because:
    # 1) the label of an account move line is an important field, we can't
    #    write a rubbish '/' in it !
    # 2) the 'name' field of the account.move.line is used in the overdue
    # letter, and '/' is not meaningful for our customer !
# TODO mig to v12
#    def action_move_create(self):
#        res = super().action_move_create()
#        for inv in self:
#            self._cr.execute(
#                "UPDATE account_move_line SET name= "
#                "CASE WHEN name='/' THEN %s "
#                "ELSE %s||' - '||name END "
#                "WHERE move_id=%s", (inv.number, inv.number, inv.move_id.id))
#            self.invalidate_cache()
#        return res

    def delete_lines_qty_zero(self):
        lines = self.env['account.move.line'].search([
            ('display_type', '=', False),
            ('move_id', 'in', self.ids),
            ('quantity', '=', 0)])
        lines.unlink()
        return True

    # for report
    def py3o_lines_layout(self):
        self.ensure_one()
        res = []
        has_sections = False
        subtotal = 0.0
        sign = self.type == 'out_refund' and -1 or 1
        for line in self.invoice_line_ids:
            if line.display_type == 'line_section':
                # insert line
                if has_sections:
                    res.append({'subtotal': subtotal})
                subtotal = 0.0  # reset counter
                has_sections = True
            else:
                if not line.display_type:
                    subtotal += line.price_subtotal * sign
            res.append({'line': line})
        if has_sections:  # insert last subtotal line
            res.append({'subtotal': subtotal})
        # res:
        # [
        #    {'line': account_invoice_line(1) with display_type=='line_section'},
        #    {'line': account_invoice_line(2) without display_type},
        #    {'line': account_invoice_line(3) without display_type},
        #    {'line': account_invoice_line(4) with display_type=='line_note'},
        #    {'subtotal': 8932.23},
        # ]
        return res

    def _compute_sales_dates(self):
        """ French law requires to set sale order dates into invoice
            returned string: "sale1 (date1), sale2 (date2) ..."
        """
        for inv in self:
            sales = inv.invoice_line_ids.mapped(
                'sale_line_ids').mapped('order_id')
            lang = inv.partner_id.commercial_partner_id.lang
            dates = ["%s (%s)" % (
                     x.name, format_date(inv.env, self.date_order))
                     for x in sales]
            inv.sale_dates = ", ".join(dates)


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    # Native order:
    # _order = "date desc, move_name desc, id"
    # Problem: when you manually create a journal entry, the
    # order of the lines is inverted when you save ! It is quite annoying for
    # the user...
    _order = "date desc, id asc"

    # In the 'account' module, we have related stored field for:
    # name (move_name), date, ref, state (parent_state),
    # journal_id, company_id, payment_id, statement_line_id,
    account_reconcile = fields.Boolean(related='account_id.reconcile')
    full_reconcile_id = fields.Many2one(string='Full Reconcile')
    matched_debit_ids = fields.One2many(string='Partial Reconcile Debit')
    matched_credit_ids = fields.One2many(string='Partial Reconcile Credit')
    reconcile_string = fields.Char(
        compute='_compute_reconcile_string', string='Reconcile', store=True)

    def show_account_move_form(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_line_form').read()[0]
        action.update({
            'res_id': self.move_id.id,
            'view_id': False,
            'views': False,
            'view_mode': 'form,tree',
        })
        return action

    @api.depends(
            'full_reconcile_id', 'matched_debit_ids', 'matched_credit_ids')
    def _compute_reconcile_string(self):
        for line in self:
            rec_str = False
            if line.full_reconcile_id:
                rec_str = line.full_reconcile_id.name
            else:
                rec_str = ', '.join([
                    'a%d' % pr.id for pr in line.matched_debit_ids + line.matched_credit_ids])
            line.reconcile_string = rec_str
