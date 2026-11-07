# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2018-2022 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import Command, api, fields, models
from odoo.exceptions import UserError


class AccountMoveUpdate(models.TransientModel):
    _name = 'account.move.update'
    _description = 'Wizard to update non-legal fields of invoice'

    invoice_id = fields.Many2one(
        'account.move', string='Invoice', required=True,
        readonly=True)
    bank_partner_id = fields.Many2one(related="invoice_id.bank_partner_id")
    move_type = fields.Selection(related='invoice_id.move_type')
    company_id = fields.Many2one(related='invoice_id.company_id')
    partner_id = fields.Many2one(related='invoice_id.partner_id')
    invoice_user_id = fields.Many2one('res.users', string='Salesperson')
    invoice_payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Term')
    invoice_date_due = fields.Date(string='Due Date')
    ref = fields.Char(string='Reference')  # field label is customized in the view
    invoice_origin = fields.Char(string='Source Document')
    partner_bank_id = fields.Many2one(
        'res.partner.bank', string='Bank Account')
    line_ids = fields.One2many(
        'account.move.line.update', 'parent_id', string='Invoice Lines')

    @api.model
    def _simple_fields2update(self):
        '''List boolean, date, datetime, char, text fields'''
        return ['ref', 'invoice_origin', 'invoice_date_due']

    @api.model
    def _m2o_fields2update(self):
        return ['invoice_payment_term_id', 'invoice_user_id', 'partner_bank_id']

    @api.model
    def _prepare_default_get(self, invoice):
        res = {'invoice_id': invoice.id, 'line_ids': []}
        for sfield in self._simple_fields2update():
            res[sfield] = invoice[sfield]
        for m2ofield in self._m2o_fields2update():
            res[m2ofield] = invoice[m2ofield].id or False
        for line in invoice.invoice_line_ids:
            res['line_ids'].append(Command.create({
                'invoice_line_id': line.id,
                'sequence': line.sequence,
                'name': line.name,
                'account_id': line.account_id.id,
                'analytic_distribution': line.analytic_distribution,
            }))
        return res

    def _prepare_invoice(self):
        vals = {}
        inv = self.invoice_id
        for sfield in self._simple_fields2update():
            if self[sfield] != inv[sfield]:
                vals[sfield] = self[sfield]
        for m2ofield in self._m2o_fields2update():
            if self[m2ofield] != inv[m2ofield]:
                vals[m2ofield] = self[m2ofield].id or False
        # when the invoice has a payment term, the due date is computed from it
        if self.invoice_payment_term_id:
            vals.pop('invoice_date_due', None)
        return vals

    @api.model
    def _line_simple_fields2update(self):
        return ["name", "analytic_distribution"]

    @api.model
    def _line_m2o_fields2update(self):
        return ['account_id']

    @api.model
    def _line_m2m_fields2update(self):
        return []

    @api.model
    def _prepare_invoice_line(self, line):
        vals = {}
        for field in self._line_simple_fields2update():
            if line[field] != line.invoice_line_id[field]:
                vals[field] = line[field]
        for field in self._line_m2o_fields2update():
            if line[field] != line.invoice_line_id[field]:
                vals[field] = line[field].id
        for field in self._line_m2m_fields2update():
            if line[field] != line.invoice_line_id[field]:
                vals[field] = [Command.set(line[field].ids)]
        return vals

    def _update_payment_term_move(self):
        self.ensure_one()
        inv = self.invoice_id
        # I don't update pay term when the invoice is partially (or fully)
        # paid because if you have a payment term with several lines
        # of the same amount, you would also have to take into account
        # the reconcile marks to put the new maturity date on the right
        # lines
        if inv.payment_state in ('partial', 'paid', 'in_payment', 'reversed'):
            raise UserError(self.env._(
                "This wizard doesn't support the update of payment "
                "terms on an invoice which is partially or fully "
                "paid."))
        prec = self.env['decimal.precision'].precision_get('Account')
        # maturity dates computed by Odoo for the new payment term:
        # key = amount in the currency precision, value = [date1, date2]
        new_maturities = {}
        for key, values in inv.needed_terms.items():
            amount = int(round(abs(values['balance']) * 10 ** prec))
            new_maturities.setdefault(amount, []).append(key['date_maturity'])
        # key = amount in the currency precision, value = [line1, line2]
        mlines = {}
        for line in inv.line_ids.filtered(
                lambda x: x.display_type == 'payment_term'):
            amount = int(round(abs(line.balance) * 10 ** prec))
            mlines.setdefault(amount, []).append(line)
        for iamount, lines in mlines.items():
            maturities = sorted(new_maturities.get(iamount, []))
            if len(lines) != len(maturities):
                raise UserError(self.env._(
                    "The new payment term '%s' doesn't have the same terms "
                    "(number of terms and/or amount) as the original one: "
                    "you can only switch to a payment term that has the "
                    "same number of terms with the same amount.",
                    self.invoice_payment_term_id.name))
            for line, maturity in zip(
                    sorted(lines,
                           key=lambda x: (x.date_maturity or x.date, x.id)),
                    maturities, strict=False):
                line.date_maturity = maturity

    def _update_due_date_move(self):
        """Report the new due date on the payment term line of the invoice.

        Without a payment term, the invoice has a single payment term line:
        its maturity date is what the ledger (and the ageing reports) use.
        """
        self.ensure_one()
        inv = self.invoice_id
        if self.invoice_payment_term_id or not self.invoice_date_due:
            return False
        term_lines = inv.line_ids.filtered(
            lambda x: x.display_type == 'payment_term')
        if (len(term_lines) != 1
                or term_lines.date_maturity == self.invoice_date_due):
            return False
        term_lines.date_maturity = self.invoice_date_due
        return True

    def run(self):
        self.ensure_one()
        inv = self.invoice_id
        updated = False
        ivals = self._prepare_invoice()
        term_updated = 'invoice_payment_term_id' in ivals
        if ivals:
            updated = True
            # Odoo allows the update of the payment term of a posted move
            # with this context (it is a readonly field otherwise)
            write_ctx = {'skip_readonly_check': True} if term_updated else {}
            inv.with_context(**write_ctx).write(ivals)
        if term_updated:
            # the write above recomputed the payment term: report the new
            # maturity dates on the payment term lines of the posted move
            self._update_payment_term_move()
        if self._update_due_date_move():
            updated = True
        for line in self.line_ids:
            ilvals = self._prepare_invoice_line(line)
            if ilvals:
                updated = True
                # note that updating analytic_distribution will delete/re-create
                # the analytic line with inverse method, we do not need additional
                # logic about that.
                line.invoice_line_id.write(ilvals)
        if updated:
            inv.message_post(body=self.env._(
                'Non-legal fields of invoice updated via the Invoice Update '
                'wizard.'))
        # Purge existing PDF
        report = self.env.ref("account.account_invoices")
        attachment = report.retrieve_attachment(inv)
        # attachment may be None
        if attachment:
            attachment.unlink()
        return True


class AccountMoveLineUpdate(models.TransientModel):
    _name = 'account.move.line.update'
    _description = 'Update non-legal fields of invoice lines'
    _order = "sequence, name"

    sequence = fields.Integer()
    parent_id = fields.Many2one(
        'account.move.update', string='Wizard', ondelete='cascade')
    invoice_line_id = fields.Many2one(
        'account.move.line', string='Invoice Line', readonly=True)
    # company_id is needed because of analytic widget in view
    company_id = fields.Many2one(related='invoice_line_id.company_id')
    display_type = fields.Selection(related="invoice_line_id.display_type")
    quantity = fields.Float(related='invoice_line_id.quantity')
    product_uom_id = fields.Many2one(related="invoice_line_id.product_uom_id")
    price_subtotal = fields.Monetary(related="invoice_line_id.price_subtotal")
    currency_id = fields.Many2one(related='invoice_line_id.currency_id')
    name = fields.Text(string='Description', required=True)
    account_id = fields.Many2one('account.account', string='Account')
    analytic_distribution = fields.Json(string="Analytic")
    analytic_precision = fields.Integer(
        default=lambda self: self.env["decimal.precision"].precision_get(
            "Percentage Analytic"
        ),
    )
