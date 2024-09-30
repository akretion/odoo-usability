# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import float_is_zero
from odoo.tools.misc import format_date

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    # By default, we can still modify "ref" when account move is posted
    # which seems a bit lazy for me...
    ref = fields.Char(states={'posted': [('readonly', True)]})
    invoice_date_due = fields.Date(tracking=True)
    invoice_payment_term_id = fields.Many2one(tracking=True)
    journal_id = fields.Many2one(tracking=True)
    fiscal_position_id = fields.Many2one(tracking=True)
    amount_total = fields.Monetary(tracking=True)
    # for invoice report
    has_discount = fields.Boolean(compute='_compute_has_discount')
    # has_attachment is useful for those who use attachment to archive
    # supplier invoices. It allows them to find supplier invoices
    # that don't have any attachment
    has_attachment = fields.Boolean(
        compute='_compute_has_attachment', search='_search_has_attachment')
    sale_dates = fields.Char(
        compute="_compute_sales_dates",
        help="This information appear on invoice qweb report "
             "(you may use it for your own report)")
        # There is a native "blocked" field (bool) on account.move.line
    # We want to have that field on invoices to improve usability
    # while keeping compatibility with the standard Odoo datamodel
    blocked = fields.Boolean(
        compute="_compute_blocked",
        inverse="_inverse_blocked",
        store=True,
        string="Dispute",
        tracking=True,
    )
    # Field search_account_id is just for search view
    search_account_id = fields.Many2one(related='line_ids.account_id')

    @api.depends("line_ids", "line_ids.blocked")
    def _compute_blocked(self):
        for move in self:
            move.blocked = any(
                [
                    l.blocked
                    for l in move.line_ids
                    if l.account_id.account_type in ("liability_payable", "asset_receivable")
                ]
            )

    def _inverse_blocked(self):
        for move in self:
            for line in move.line_ids.filtered(
                lambda l: l.account_id.account_type in ("liability_payable", "asset_receivable")
            ):
                line.blocked = move.blocked

    def _compute_has_discount(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        for inv in self:
            has_discount = False
            for line in inv.invoice_line_ids:
                if line.display_type == 'product' and not float_is_zero(line.discount, precision_digits=prec):
                    has_discount = True
                    break
            inv.has_discount = has_discount

    def _compute_has_attachment(self):
        iao = self.env['ir.attachment']
        for move in self:
            if iao.search_count([
                    ('res_model', '=', 'account.move'),
                    ('res_id', '=', move.id),
                    ('type', '=', 'binary'),
                    ('company_id', '=', move.company_id.id)]):
                move.has_attachment = True
            else:
                move.has_attachment = False

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

    def _reverse_moves(self, default_values_list=None, cancel=False):
        reverse_moves = super()._reverse_moves(
            default_values_list=default_values_list, cancel=cancel)
        # In the simple scenario 1 invoice -> 1 refund, we add a message in the chatter
        # of the invoice and in the chatter of the refund
        if len(self) == 1 and len(reverse_moves) == 1:
            self.message_post(body=_("A reverse journal entry <a href=# data-oe-model=account.move data-oe-id=%d>%s</a> has been generated.") % (reverse_moves.id, reverse_moves.display_name))
            reverse_moves.message_post(body=_("This journal entry has been generated as the reverse of <a href=# data-oe-model=account.move data-oe-id=%d>%s</a>.") % (self.id, self.display_name))
        return reverse_moves

    def delete_lines_qty_zero(self):
        lines = self.env['account.move.line'].search([
            ('display_type', '=', 'product'),
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
        sign = self.move_type == 'out_refund' and -1 or 1
        # Warning: the order of invoice line is forced in the view
        # <tree editable="bottom" default_order="sequence, date desc, move_name desc, id"
        # it's not the same as the _order in the class AccountMoveLine
        lines = self.env['account.move.line'].search([('display_type', 'in', ('product', 'line_section', 'line_note')), ('move_id', '=', self.id)], order="sequence, date desc, move_name desc, id")
        for line in lines:
            if line.display_type == 'line_section':
                # insert line
                if has_sections:
                    res.append({'subtotal': subtotal})
                subtotal = 0.0  # reset counter
                has_sections = True
            else:
                if line.display_type == 'product':
                    subtotal += line.price_subtotal * sign
            res.append({'line': line})
        if has_sections:  # insert last subtotal line
            res.append({'subtotal': subtotal})
        # res:
        # [
        #    {'line': account_invoice_line(1) with display_type=='line_section'},
        #    {'line': account_invoice_line(2) with display_type=='product'},
        #    {'line': account_invoice_line(3) with display_type=='product'},
        #    {'line': account_invoice_line(4) with display_type=='line_note'},
        #    {'subtotal': 8932.23},
        # ]
        return res

    def _compute_sales_dates(self):
        """ French law requires to set sale order dates into invoice
            returned string: "sale1 (date1), sale2 (date2) ..."
        """
        for move in self:
            sales = move.invoice_line_ids.mapped(
                'sale_line_ids').mapped('order_id')
            dates = ["%s (%s)" % (
                     x.name, format_date(move.env, x.date_order))
                     for x in sales]
            move.sale_dates = ", ".join(dates)

    # allow to manually create moves not only in general journals,
    # but also in cash journal and check journals (= bank journals not linked to a bank account)
    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for move in self:
            if move.invoice_filter_type_domain:
                super(AccountMove, move)._compute_suitable_journal_ids()
            else:
                company_id = move.company_id.id or self.env.company.id
                domain = expression.AND([
                        [('company_id', '=', company_id)],
                        expression.OR([
                            [('type', 'in', ('general', 'cash'))],
                            [('type', '=', 'bank'), ('bank_account_id', '=', False)]
                            ])
                        ])
                move.suitable_journal_ids = self.env['account.journal'].search(domain)

    def button_draft(self):
        super().button_draft()
        # Delete attached pdf invoice
        try:
            report_invoice = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
        except IndexError:
            report_invoice = False
        if report_invoice and report_invoice.attachment:
            for move in self.filtered(lambda x: x.move_type in ('out_invoice', 'out_refund')):
                # The pb is that the filename is dynamic and related to move.state
                # in v12, the feature was native and they used that kind of code:
                # with invoice.env.do_in_draft():
                #    invoice.number, invoice.state = invoice.move_name, 'open'
                #    attachment = self.env.ref('account.account_invoices').retrieve_attachment(invoice)
                # But do_in_draft() doesn't exists in v14
                # If you know how we could do that, please update the code below
                attachment = self.env['ir.attachment'].search([
                    ('name', '=', self._get_invoice_attachment_name()),
                    ('res_id', '=', move.id),
                    ('res_model', '=', self._name),
                    ('type', '=', 'binary'),
                    ], limit=1)
                if attachment:
                    attachment.unlink()

    def _get_invoice_attachment_name(self):
        self.ensure_one()
        return '%s.pdf' % (self.name and self.name.replace('/', '_') or 'INV')

    def _get_accounting_date(self, invoice_date, has_tax):
        # On vendor bills/refunds, we want date = invoice_date unless
        # we have a company tax_lock_date and the invoice has taxes
        # and invoice_date <= tax_lock_date
        date = super()._get_accounting_date(invoice_date, has_tax)
        if self.is_purchase_document(include_receipts=True):
            tax_lock_date = self.company_id.tax_lock_date
            if invoice_date and tax_lock_date and has_tax and invoice_date <= tax_lock_date:
                invoice_date = tax_lock_date + timedelta(days=1)
            date = invoice_date
        return date


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
    # for optional display in tree view
    product_barcode = fields.Char(related='product_id.barcode', string="Product Barcode")

    def show_account_move_form(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            'account.action_move_line_form')
        action.update({
            'res_id': self.move_id.id,
            'view_id': False,
            'views': False,
            'view_mode': 'form,tree',
        })
        return action

    def update_matching_number(self):
        records = self.search([("matching_number", "=", "P")])
        _logger.info(f"Update partial reconcile number for {len(records)} lines")
        records._compute_matching_number()

#    def _compute_matching_number(self):
        # TODO maybe it will be better to have the same maching_number for
        # all partial so it will be easier to group by
#        super()._compute_matching_number()
#        for record in self:
#            if record.matching_number == "P":
#                record.matching_number = ", ".join([
#                    "a%d" % pr.id
#                    for pr in record.matched_debit_ids + record.matched_credit_ids
#                ])

    def _compute_name(self):
        # This is useful when you want to have the product code in a dedicated
        # column in your customer invoice report
        # The same ir.config_parameter is used in sale_usability,
        # purchase_usability and account_usability
        no_product_code_param = self.env['ir.config_parameter'].sudo().get_param(
            'usability.line_name_no_product_code')
        if no_product_code_param and no_product_code_param == 'True':
            self = self.with_context(display_default_code=False)
        return super()._compute_name()

    def reconcile(self):
        """Explicit error message if unposted lines"""
        unposted_ids = self.filtered(lambda l: l.move_id.state != "posted")
        if unposted_ids:
            m = _("Please post the following entries before reconciliation :")
            sep = "\n - "
            unpost = sep.join([am.display_name for am in unposted_ids.move_id])
            raise UserError(m + sep + unpost)

        return super().reconcile()
