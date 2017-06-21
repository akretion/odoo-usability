# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError
import openerp.addons.decimal_precision as dp


class AccountInvoiceUpdate(models.TransientModel):
    _name = 'account.invoice.update'
    _description = 'Wizard to update non-legal fields of invoice'

    invoice_id = fields.Many2one(
        'account.invoice', string='Invoice', required=True,
        readonly=True)
    type = fields.Selection(related='invoice_id.type', readonly=True)
    company_id = fields.Many2one(
        related='invoice_id.company_id', readonly=True)
    commercial_partner_id = fields.Many2one(
        related='invoice_id.commercial_partner_id', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson')
    # I use the same field name as the original invoice field name
    # even if it the name is "bad"
    # Updating payment_term will not work if you use
    # the OCA module account_constraints (you will just get an error)
    payment_term = fields.Many2one(
        'account.payment.term', string='Payment Terms')
    reference = fields.Char(string='Invoice Reference')
    name = fields.Char(string='Reference/Description')
    origin = fields.Char(string='Source Document')
    comment = fields.Text('Additional Information')
    partner_bank_id = fields.Many2one(
        'res.partner.bank', string='Bank Account')
    line_ids = fields.One2many(
        'account.invoice.line.update', 'parent_id', string='Invoice Lines')

    @api.model
    def _simple_fields2update(self):
        '''List boolean, date, datetime, char, text fields'''
        return ['reference', 'name', 'origin', 'comment']

    @api.model
    def _m2o_fields2update(self):
        return ['payment_term', 'user_id', 'partner_bank_id']

    @api.model
    def _prepare_default_get(self, invoice):
        res = {'invoice_id': invoice.id, 'line_ids': []}
        for sfield in self._simple_fields2update():
            res[sfield] = invoice[sfield]
        for m2ofield in self._m2o_fields2update():
            res[m2ofield] = invoice[m2ofield].id or False
        for line in invoice.invoice_line:
            res['line_ids'].append({
                'invoice_line_id': line.id,
                'name': line.name,
                'quantity': line.quantity,
                'price_subtotal': line.price_subtotal,
                })
        return res

    @api.model
    def default_get(self, fields_list):
        res = super(AccountInvoiceUpdate, self).default_get(fields_list)
        assert self._context.get('active_model') == 'account.invoice',\
            'active_model should be account.invoice'
        inv = self.env['account.invoice'].browse(self._context['active_id'])
        res = self._prepare_default_get(inv)
        return res

    @api.onchange('type')
    def type_on_change(self):
        res = {'domain': {}}
        if self.type in ('out_invoice', 'out_refund'):
            res['domain']['partner_bank_id'] =\
                "[('partner_id.ref_companies', 'in', [company_id])]"
        else:
            res['domain']['partner_bank_id'] =\
                "[('partner_id', '=', commercial_partner_id)]"
        return res

    @api.multi
    def _prepare_invoice(self):
        vals = {}
        inv = self.invoice_id
        for sfield in self._simple_fields2update():
            if self[sfield] != inv[sfield]:
                vals[sfield] = self[sfield]
        for m2ofield in self._m2o_fields2update():
            if self[m2ofield] != inv[m2ofield]:
                vals[m2ofield] = self[m2ofield].id or False
        if 'payment_term' in vals:
            pterm_list = self.payment_term.compute(
                value=1, date_ref=inv.date_invoice)[0]
            if pterm_list:
                vals['date_due'] = max(line[0] for line in pterm_list)
        return vals

    @api.model
    def _prepare_invoice_line(self, line):
        vals = {}
        if line.name != line.invoice_line_id.name:
            vals['name'] = line.name
        return vals

    @api.multi
    def _prepare_move(self):
        mvals = {}
        inv = self.invoice_id
        ini_ref = inv.move_id.ref
        ref = inv.reference or inv.name
        if ini_ref != ref:
            mvals['ref'] = ref
        return mvals

    @api.multi
    def _update_payment_term_move(self):
        self.ensure_one()
        inv = self.invoice_id
        if (
                self.payment_term and
                self.payment_term != inv.payment_term and
                inv.move_id and
                inv.move_id.period_id.state == 'draft'):
            # I don't update pay term when the invoice is partially (or fully)
            # paid because if you have a payment term with several lines
            # of the same amount, you would also have to take into account
            # the reconcile marks to put the new maturity date on the right
            # lines
            if inv.payment_ids:
                raise UserError(_(
                    "This wizard doesn't support the update of payment "
                    "terms on an invoice which is partially or fully "
                    "paid."))
            prec = self.env['decimal.precision'].precision_get('Account')
            term_res = self.payment_term.compute(
                inv.amount_total, inv.date_invoice)[0]
            new_pterm = {}  # key = int(amount * 100), value = [date1, date2]
            for entry in term_res:
                amount = int(entry[1] * 10 * prec)
                if amount in new_pterm:
                    new_pterm[amount].append(entry[0])
                else:
                    new_pterm[amount] = [entry[0]]
            mlines = {}  # key = int(amount * 100), value : [line1, line2]
            for line in inv.move_id.line_id:
                if line.account_id == inv.account_id:
                    amount = int(abs(line.credit - line.debit) * 10 * prec)
                    if amount in mlines:
                        mlines[amount].append(line)
                    else:
                        mlines[amount] = [line]
            for iamount, lines in mlines.iteritems():
                if len(lines) != len(new_pterm.get(iamount, [])):
                    raise UserError(_(
                        "The original payment term '%s' doesn't have the "
                        "same terms (number of terms and/or amount) as the "
                        "new payment term '%s'. You can only switch to a "
                        "payment term that has the same number of terms "
                        "with the same amount.") % (
                        inv.payment_term.name, self.payment_term.name))
                for line in lines:
                    line.date_maturity = new_pterm[iamount].pop()

    @api.multi
    def run(self):
        self.ensure_one()
        inv = self.invoice_id
        updated = False
        # re-write date_maturity on move line
        self._update_payment_term_move()
        ivals = self._prepare_invoice()
        if ivals:
            updated = True
            inv.write(ivals)
        for line in self.line_ids:
            ilvals = self._prepare_invoice_line(line)
            if ilvals:
                updated = True
                line.invoice_line_id.write(ilvals)
        if inv.move_id and inv.move_id.period_id.state == 'draft':
            mvals = self._prepare_move()
            if mvals:
                inv.move_id.write(mvals)
        if updated:
            inv.message_post(_(
                'Non-legal fields of invoice updated via the Invoice Update '
                'wizard.'))
        return True


class AccountInvoiceLineUpdate(models.TransientModel):
    _name = 'account.invoice.line.update'
    _description = 'Update non-legal fields of invoice lines'

    parent_id = fields.Many2one(
        'account.invoice.update', string='Wizard', ondelete='cascade')
    invoice_line_id = fields.Many2one(
        'account.invoice.line', string='Invoice Line', readonly=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(
        string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        readonly=True)
    price_subtotal = fields.Float(
        string='Amount', readonly=True, digits=dp.get_precision('Account'))
