# Copyright 2015-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta
import logging

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import float_is_zero
from odoo.tools.misc import format_date

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

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
    # The native "blocked" field (bool) on account.move.line has been removed in v18
#    blocked = fields.Boolean(
#        compute="_compute_blocked",
#        inverse="_inverse_blocked",
#        store=True,
#        string="Dispute",
#        tracking=True,
#    )
    # Field search_account_id is just for search view
    search_account_id = fields.Many2one(related='line_ids.account_id')

#    @api.depends("line_ids", "line_ids.blocked")
#    def _compute_blocked(self):
#        for move in self:
#            move.blocked = any(
#                [
#                    l.blocked
#                    for l in move.line_ids
#                    if l.account_id.account_type in ("liability_payable", "asset_receivable")
#                ]
#            )

#    def _inverse_blocked(self):
#        for move in self:
#            for line in move.line_ids.filtered(
#                lambda l: l.account_id.account_type in ("liability_payable", "asset_receivable")
#            ):
#                line.blocked = move.blocked

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
            search_res = self.env['ir.attachment'].with_context(skip_res_field_check=True).search_read([
                ('res_model', '=', 'account.move'),
                ('type', '=', 'binary'),
                ('res_id', '!=', False)], ['res_id'])
            for att in search_res:
                att_inv_ids[att['res_id']] = True
        res = [('id', value and 'in' or 'not in', list(att_inv_ids))]
        return res

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

# There is no more attachment by default on invoice reports...
# TODO check what's the editor strategy on this
#    def button_draft(self):
        # Delete attached pdf invoice
#        for move in self.filtered(lambda x: x.move_type in ('out_invoice', 'out_refund')):
#            for report_xmlid in ('account.account_invoices', 'account.account_invoices_without_payment'):
#                report = self.env.ref(report_xmlid)
#                attach = report.retrieve_attachment(move)
#                if attach:
#                    attach.unlink()
#        super().button_draft()

    def _get_accounting_date(self, invoice_date, has_tax, lock_dates=None):
        # On vendor bills/refunds, we want date = invoice_date unless
        # we have a company tax_lock_date and the invoice has taxes
        # and invoice_date <= tax_lock_date
        date = super()._get_accounting_date(invoice_date, has_tax, lock_dates=lock_dates)
        lock_dates = lock_dates or self._get_violated_lock_dates(invoice_date, has_tax)
        if self.is_purchase_document(include_receipts=True) and invoice_date:
            if lock_dates:
                date = max([entry[0] for entry in lock_dates]) + timedelta(1)
            else:
               date = invoice_date
        return date
