# Copyright 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# Copyright 2018-2019 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class AccountInvoiceUpdate(models.TransientModel):
    _name = 'account.invoice.update'
    _description = 'Wizard to update non-legal fields of invoice'

    invoice_id = fields.Many2one(
        'account.invoice', string='Invoice', required=True,
        readonly=True)
    type = fields.Selection(related='invoice_id.type', readonly=True)
    company_id = fields.Many2one(
        related='invoice_id.company_id', readonly=True)
    partner_id = fields.Many2one(
        related='invoice_id.partner_id', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson')
    payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Term')
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
        return ['payment_term_id', 'user_id', 'partner_bank_id']

    @api.model
    def _prepare_default_get(self, invoice):
        res = {'invoice_id': invoice.id, 'line_ids': []}
        for sfield in self._simple_fields2update():
            res[sfield] = invoice[sfield]
        for m2ofield in self._m2o_fields2update():
            res[m2ofield] = invoice[m2ofield].id or False
        for line in invoice.invoice_line_ids:
            aa_tags = line.analytic_tag_ids
            aa_tags = [(6, 0, aa_tags.ids)] if aa_tags else False
            res['line_ids'].append([0, 0, {
                'invoice_line_id': line.id,
                'name': line.name,
                'quantity': line.quantity,
                'price_subtotal': line.price_subtotal,
                'account_analytic_id': line.account_analytic_id.id,
                'analytic_tag_ids': aa_tags,
                'display_type': line.display_type,
            }])
        return res

    @api.onchange('type')
    def type_on_change(self):
        res = {'domain': {}}
        if self.type in ('out_invoice', 'out_refund'):
            res['domain']['partner_bank_id'] =\
                "[('partner_id.ref_company_ids', 'in', [company_id])]"
        else:
            res['domain']['partner_bank_id'] =\
                "[('partner_id', '=', partner_id)]"
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
        if 'payment_term_id' in vals:
            pterm_list = self.payment_term_id.compute(
                value=1, date_ref=inv.date_invoice)[0]
            if pterm_list:
                vals['date_due'] = max(line[0] for line in pterm_list)
        return vals

    @api.model
    def _line_simple_fields2update(self):
        return ["name",]

    @api.model
    def _line_m2o_fields2update(self):
        return ["account_analytic_id",]

    @api.model
    def _line_m2m_fields2update(self):
        return ["analytic_tag_ids",]

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
                vals[field] = [(6, 0, line[field].ids)]
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
    def _get_matching_inv_line(self, move_line):
        """ Find matching invoice line by product """
        # TODO make it accept more case as lines won't
        # be grouped unless journal.group_invoice_line is True
        inv_line = self.invoice_id.invoice_line_ids.filtered(
            lambda rec: rec.product_id == move_line.product_id)
        if len(inv_line) != 1:
            raise UserError(
                "Cannot match a single invoice line to move line %s" %
                move_line.name)
        return inv_line

    @api.multi
    def _prepare_move_line(self, inv_line):
        mlvals = {}
        inv_line_upd = self.line_ids.filtered(
            lambda rec: rec.invoice_line_id == inv_line)

        ini_aa = inv_line.account_analytic_id
        new_aa = inv_line_upd.account_analytic_id

        if ini_aa != new_aa:
            mlvals['analytic_account_id'] = new_aa.id

        ini_aa_tags = inv_line.analytic_tag_ids
        new_aa_tags = inv_line_upd.analytic_tag_ids

        if ini_aa_tags != new_aa_tags:
            mlvals['analytic_tag_ids'] = [(6, None, new_aa_tags.ids)]
        return mlvals

    @api.multi
    def _prepare_analytic_line(self, inv_line):
        alvals = {}
        inv_line_upd = self.line_ids.filtered(
            lambda rec: rec.invoice_line_id == inv_line)

        ini_aa = inv_line.account_analytic_id
        new_aa = inv_line_upd.account_analytic_id

        if ini_aa != new_aa:
            alvals['account_id'] = new_aa.id

        ini_aa_tags = inv_line.analytic_tag_ids
        new_aa_tags = inv_line_upd.analytic_tag_ids

        if ini_aa_tags != new_aa_tags:
            alvals['tag_ids'] = [(6, None, new_aa_tags.ids)]
        return alvals

    @api.multi
    def _update_payment_term_move(self):
        self.ensure_one()
        inv = self.invoice_id
        if (
                self.payment_term_id and
                self.payment_term_id != inv.payment_term_id and
                inv.move_id):
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
            term_res = self.payment_term_id.compute(
                inv.amount_total, inv.date_invoice)[0]
            new_pterm = {}  # key = int(amount * 100), value = [date1, date2]
            for entry in term_res:
                amount = int(entry[1] * 10 * prec)
                if amount in new_pterm:
                    new_pterm[amount].append(entry[0])
                else:
                    new_pterm[amount] = [entry[0]]
            mlines = {}  # key = int(amount * 100), value : [line1, line2]
            for line in inv.move_id.line_ids:
                if line.account_id == inv.account_id:
                    amount = int(abs(line.credit - line.debit) * 10 * prec)
                    if amount in mlines:
                        mlines[amount].append(line)
                    else:
                        mlines[amount] = [line]
            for iamount, lines in mlines.items():
                if len(lines) != len(new_pterm.get(iamount, [])):
                    raise UserError(_(
                        "The original payment term '%s' doesn't have the "
                        "same terms (number of terms and/or amount) as the "
                        "new payment term '%s'. You can only switch to a "
                        "payment term that has the same number of terms "
                        "with the same amount.") % (
                        inv.payment_term_id.name, self.payment_term_id.name))
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
        if inv.move_id:
            mvals = self._prepare_move()
            if mvals:
                inv.move_id.write(mvals)
            for ml in inv.move_id.line_ids.filtered(
                    # we are only interested in invoice lines, not tax lines
                    lambda rec: bool(rec.product_id)
            ):
                if ml.credit == 0.0:
                    continue
                inv_line = self._get_matching_inv_line(ml)
                mlvals = self._prepare_move_line(inv_line)
                if mlvals:
                    updated = True
                    ml.write(mlvals)
                aalines = ml.analytic_line_ids
                alvals = self._prepare_analytic_line(inv_line)
                if aalines and alvals:
                    updated = True
                    if ('account_id' in alvals and
                            alvals['account_id'] is False):
                        former_aa = inv_line.account_analytic_id
                        to_remove_aalines = aalines.filtered(
                            lambda rec: rec.account_id == former_aa)
                        # remove existing analytic line
                        to_remove_aalines.unlink()
                    else:
                        aalines.write(alvals)
                elif 'account_id' in alvals:
                    # Create analytic lines if analytic account
                    # is added later
                    ml.create_analytic_lines()
        for line in self.line_ids:
            ilvals = self._prepare_invoice_line(line)
            if ilvals:
                updated = True
                line.invoice_line_id.write(ilvals)
        if updated:
            inv.message_post(body=_(
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
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    quantity = fields.Float(
        string='Quantity', digits=dp.get_precision('Product Unit of Measure'),
        readonly=True)
    price_subtotal = fields.Float(
        string='Amount', readonly=True, digits=dp.get_precision('Account'))
    account_analytic_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many(
        'account.analytic.tag', string='Analytic Tags')
