# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    origin = fields.Char(track_visibility='onchange')
    reference = fields.Char(track_visibility='onchange')
    sent = fields.Boolean(track_visibility='onchange')
    date_invoice = fields.Date(track_visibility='onchange')
    date_due = fields.Date(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    partner_bank_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    amount_total = fields.Monetary(track_visibility='onchange')
    # for those fields, the 'account' module sets track_visibility='always':
    partner_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    amount_untaxed = fields.Monetary(track_visibility='onchange')
    # I want to see the number of cancelled invoice in chatter
    move_id = fields.Many2one(track_visibility='onchange')
    # for invoice report
    has_discount = fields.Boolean(
        compute='_compute_has_discount', readonly=True)
    # has_attachment is useful for those who use attachment to archive
    # supplier invoices. It allows them to find supplier invoices
    # that don't have any attachment
    has_attachment = fields.Boolean(
        compute='_compute_has_attachment',
        search='_search_has_attachment', readonly=True)

    @api.multi
    def _compute_has_discount(self):
        prec = self.env['decimal.precision'].precision_get('Discount')
        for inv in self:
            has_discount = False
            for line in inv.invoice_line_ids:
                if not float_is_zero(line.discount, precision_digits=prec):
                    has_discount = True
                    break
            inv.has_discount = has_discount

    def _compute_has_attachment(self):
        iao = self.env['ir.attachment']
        for inv in self:
            if iao.search([
                    ('res_model', '=', 'account.invoice'),
                    ('res_id', '=', inv.id),
                    ('type', '=', 'binary'),
                    ('company_id', '=', inv.company_id.id)], limit=1):
                inv.has_attachment = True
            else:
                inv.has_attachment = False

    def _search_has_attachment(self, operator, value):
        att_inv_ids = {}
        if operator == '=':
            search_res = self.env['ir.attachment'].search_read([
                ('res_model', '=', 'account.invoice'),
                ('type', '=', 'binary'),
                ('res_id', '!=', False)], ['res_id'])
            for att in search_res:
                att_inv_ids[att['res_id']] = True
        res = [('id', value and 'in' or 'not in', att_inv_ids.keys())]
        return res

    # I really hate to see a "/" in the 'name' field of the account.move.line
    # generated from customer invoices linked to the partners' account because:
    # 1) the label of an account move line is an important field, we can't
    #    write a rubbish '/' in it !
    # 2) the 'name' field of the account.move.line is used in the overdue
    # letter, and '/' is not meaningful for our customer !
    @api.multi
    def action_move_create(self):
        res = super(AccountInvoice, self).action_move_create()
        for inv in self:
            self._cr.execute(
                "UPDATE account_move_line SET name= "
                "CASE WHEN name='/' THEN %s "
                "ELSE %s||' - '||name END "
                "WHERE move_id=%s", (inv.number, inv.number, inv.move_id.id))
            self.invalidate_cache()
        return res

    def delete_lines_qty_zero(self):
        lines = self.env['account.invoice.line'].search([
            ('invoice_id', 'in', self.ids), ('quantity', '=', 0)])
        lines.unlink()
        return True


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # In the 'account' module, we have related stored field for:
    # company_id, partner_id, currency_id
    invoice_type = fields.Selection(
        related='invoice_id.type', store=True, readonly=True)
    date_invoice = fields.Date(
        related='invoice_id.date_invoice', store=True, readonly=True)
    commercial_partner_id = fields.Many2one(
        related='invoice_id.partner_id.commercial_partner_id',
        store=True, readonly=True)
    state = fields.Selection(
        related='invoice_id.state', store=True, readonly=True,
        string='Invoice State')
    invoice_number = fields.Char(
        related='invoice_id.move_id.name', store=True, readonly=True,
        string='Invoice Number')


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.multi
    @api.depends(
        'name', 'currency_id', 'company_id', 'company_id.currency_id', 'code')
    def name_get(self):
        res = []
        if self._context.get('journal_show_code_only'):
            for journal in self:
                res.append((journal.id, journal.code))
            return res
        else:
            for journal in self:
                currency = journal.currency_id or\
                    journal.company_id.currency_id
                name = "[%s] %s (%s)" % (
                    journal.code, journal.name, currency.name)
                res.append((journal.id, name))
            return res

    # Also search on start of 'code', not only on 'name'
    @api.model
    def name_search(
            self, name='', args=None, operator='ilike', limit=80):
        if args is None:
            args = []
        if name:
            jrls = self.search(
                [('code', '=ilike', name + '%')] + args, limit=limit)
            if jrls:
                return jrls.name_get()
        return super(AccountJournal, self).name_search(
            name=name, args=args, operator=operator, limit=limit)


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.multi
    def name_get(self):
        if self._context.get('account_account_show_code_only'):
            res = []
            for record in self:
                res.append((record.id, record.code))
            return res
        else:
            return super(AccountAccount, self).name_get()


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.multi
    def name_get(self):
        if self._context.get('analytic_account_show_code_only'):
            res = []
            for record in self:
                res.append((
                    record.id,
                    record.code or record._get_one_full_name(record)))
            return res
        else:
            return super(AccountAnalyticAccount, self).name_get()

    _sql_constraints = [(
        'code_company_unique',
        'unique(code, company_id)',
        'An analytic account with the same code already '
        'exists in the same company!')]


class AccountMove(models.Model):
    _inherit = 'account.move'

    default_move_line_name = fields.Char(
        string='Default Label', states={'posted': [('readonly', True)]})
    # By default, we can still modify "ref" when account move is posted
    # which seems a bit lazy for me...
    ref = fields.Char(states={'posted': [('readonly', True)]})


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    # Native order:
    # _order = "date desc, id desc"
    # Problem: when you manually create a journal entry, the
    # order of the lines is inverted when you save ! It is quite annoying for
    # the user...
    _order = "date desc, id asc"

    # Update field only to add a string (there is no string in account module)
    invoice_id = fields.Many2one(string='Invoice')

    @api.onchange('credit')
    def _credit_onchange(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        if (
                not float_is_zero(self.credit, precision_digits=prec) and
                not float_is_zero(self.debit, precision_digits=prec)):
            self.debit = 0

    @api.onchange('debit')
    def _debit_onchange(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        if (
                not float_is_zero(self.debit, precision_digits=prec) and
                not float_is_zero(self.credit, precision_digits=prec)):
            self.credit = 0

    @api.onchange('currency_id', 'amount_currency')
    def _amount_currency_change(self):
        prec = self.env['decimal.precision'].precision_get('Account')
        if (
                self.currency_id and
                self.amount_currency and
                float_is_zero(self.credit, precision_digits=prec) and
                float_is_zero(self.debit, precision_digits=prec)):
            date = self.date or None
            amount_company_currency = self.currency_id.with_context(
                date=date).compute(
                    self.amount_currency, self.env.user.company_id.currency_id)
            precision = self.env['decimal.precision'].precision_get('Account')
            if float_compare(
                    amount_company_currency, 0,
                    precision_digits=precision) == -1:
                self.debit = amount_company_currency * -1
            else:
                self.credit = amount_company_currency

    @api.multi
    def show_account_move_form(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account', 'action_move_line_form')
        action.update({
            'res_id': self.move_id.id,
            'view_id': False,
            'views': False,
            'view_mode': 'form,tree',
        })
        return action


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    start_date = fields.Date(
        compute='_compute_dates', string='Start Date', readonly=True,
        store=True)
    end_date = fields.Date(
        compute='_compute_dates', string='End Date', readonly=True,
        store=True)

    @api.multi
    @api.depends('line_ids.date')
    def _compute_dates(self):
        for st in self:
            dates = [line.date for line in st.line_ids]
            st.start_date = dates and min(dates) or False
            st.end_date = dates and max(dates) or False


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'
    # Native order is:
    # _order = 'statement_id desc, sequence, id desc'
    _order = 'statement_id desc, date desc, sequence, id desc'

    # Disable guessing for reconciliation
    # because my experience with several customers shows that it is a problem
    # in the following scenario : move line 'x' has been "guessed" by OpenERP
    # to be reconciled with a statement line 'Y' at the end of the bank
    # statement, but it is a mistake because it should be reconciled with
    # statement line 'B' at the beginning of the bank statement
    # When the user is on statement line 'B', he tries to select
    # move line 'x', but it can't find it... because it is already "reserved"
    # by the guess of OpenERP for statement line 'Y' ! To solve this problem,
    # the user must go to statement line 'Y' and unselect move line 'x'
    # and then come back on statement line 'B' and select move line 'A'...
    # but non super-expert users can't do that because it is impossible to
    # figure out that the fact that the user can't find move line 'x'
    # is caused by this.
    # Set search_reconciliation_proposition to False by default
    # TODO: re-write in v10
    # def get_data_for_reconciliations(
    #        self, cr, uid, ids, excluded_ids=None,
    #        search_reconciliation_proposition=False, context=None):
    #    # Make variable name shorted for PEP8 !
    #    search_rec_prop = search_reconciliation_proposition
    #    return super(AccountBankStatementLine, self).\
    #        get_data_for_reconciliations(
    #            cr, uid, ids, excluded_ids=excluded_ids,
    #            search_reconciliation_proposition=search_rec_prop,
    #            context=context)

    def _prepare_reconciliation_move(self, move_ref):
        vals = super(AccountBankStatementLine, self).\
            _prepare_reconciliation_move(move_ref)
        # By default, ref contains the name of the statement + name of the
        # statement line. It causes 2 problems:
        # 1) The 'ref' field is too big
        # 2) The name of the statement line is already written in the name of
        # the move line -> not useful to have the info 2 times
        # In the end, I think it's better to just put nothing (we could write
        # the name of the statement which has the account number, but it
        # doesn't bring any useful info to the accountant)
        # The only "good" thing to do would be to have a sequence per
        # statement line and write it in this 'ref' field
        # But that would required an additionnal field on statement lines
        vals['ref'] = False
        return vals

    @api.multi
    def show_account_move(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account', 'action_move_journal_line')
        if self.journal_entry_ids:
            action.update({
                'views': False,
                'view_id': False,
                'view_mode': 'form,tree',
                'res_id': self.journal_entry_ids[0].id,
                })
            return action
        else:
            raise UserError(_(
                'No journal entry linked to this bank statement line.'))


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    note = fields.Text(translate=True)

    @api.model
    def get_fiscal_position_no_partner(
            self, company_id=None, vat_subjected=False, country_id=None):
        '''This method is inspired by the method get_fiscal_position()
        in odoo/addons/account/partner.py : it uses the same algo
        but without a real partner.
        Returns a recordset of fiscal position, or False'''
        domains = [[
            ('auto_apply', '=', True),
            ('vat_required', '=', vat_subjected),
            ('company_id', '=', company_id)]]
        if vat_subjected:
            domains += [[
                ('auto_apply', '=', True),
                ('vat_required', '=', False),
                ('company_id', '=', company_id)]]

        for domain in domains:
            if country_id:
                fps = self.search(
                    domain + [('country_id', '=', country_id)], limit=1)
                if fps:
                    return fps[0]

                fps = self.search(
                    domain +
                    [('country_group_id.country_ids', '=', country_id)],
                    limit=1)
                if fps:
                    return fps[0]

            fps = self.search(
                domain +
                [('country_id', '=', None), ('country_group_id', '=', None)],
                limit=1)
            if fps:
                return fps[0]
        return False


class AccountReconcileModel(models.Model):
    _inherit = 'account.reconcile.model'

    @api.onchange('name')
    def onchange_name(self):
        # Do NOT copy by default name on label
        # Because it's much better to have the bank statement line label as
        # label of the counter-part move line, then the label of the button
        assert True  # Stupid line of code just to have something...
