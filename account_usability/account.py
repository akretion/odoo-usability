# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError
from itertools import groupby


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
    # for invoice report
    has_discount = fields.Boolean(
        compute='_compute_has_discount', readonly=True)

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

    # I really hate to see a "/" in the 'name' field of the account.move.line
    # generated from customer invoices linked to the partners' account because:
    # 1) the label of an account move line is an important field, we can't
    #    write a rubbish '/' in it !
    # 2) the 'name' field of the account.move.line is used in the overdue letter,
    # and '/' is not meaningful for our customer !
    # TODO port to v10
    #@api.multi
    #def action_number(self):
    #    res = super(AccountInvoice, self).action_number()
    #    for inv in self:
    #        self._cr.execute(
    #            "UPDATE account_move_line SET name= "
    #            "CASE WHEN name='/' THEN %s "
    #            "ELSE %s||' - '||name END "
    #            "WHERE move_id=%s", (inv.number, inv.number, inv.move_id.id))
    #        self.invalidate_cache()
    #    return res


    # for report
    @api.multi
    def py3o_lines_layout(self):
        self.ensure_one()
        res1 = []
        # [
        #    {'categ': categ(6), 'lines': [l1, l2], 'subtotal': 23.32},
        #    {'categ': categ(1), 'lines': [l3, l4, l5], 'subtotal': 12.42},
        # ]
        for categ, lines in\
                groupby(self.invoice_line_ids, lambda l: l.layout_category_id):
            entry = {'lines': [], 'categ': categ}
            if categ.subtotal:
                entry['subtotal'] = 0.0
            for line in lines:
                entry['lines'].append(line)
                if 'subtotal' in entry:
                    entry['subtotal'] += line.price_subtotal
            res1.append(entry)
        res2 = []
        if len(res1) == 1 and not res1[0]['categ']:
            # No category at all
            for l in res1[0]['lines']:
                res2.append({'line': l})
        else:
            # TODO : gérer qd il n'y a pas de categ
            for ldict in res1:
                res2.append({'categ': ldict['categ']})
                for line in ldict['lines']:
                    res2.append({'line': line})
                if 'subtotal' in ldict:
                    res2.append({'subtotal': ldict['subtotal']})
        # res2:
        # [
        #    {'categ': categ(1)},
        #    {'line': invoice_line(2)},
        #    {'line': invoice_line(3)},
        #    {'subtotal': 8932.23},
        # ]
        return res2


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
    def name_get(self):
        if self._context.get('journal_show_code_only'):
            res = []
            for record in self:
                res.append((record.id, record.code))
            return res
        else:
            return super(AccountJournal, self).name_get()


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


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

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


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

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
    #def get_data_for_reconciliations(
    #        self, cr, uid, ids, excluded_ids=None,
    #        search_reconciliation_proposition=False, context=None):
    #    # Make variable name shorted for PEP8 !
    #    search_rec_prop = search_reconciliation_proposition
    #    return super(AccountBankStatementLine, self).\
    #        get_data_for_reconciliations(
    #            cr, uid, ids, excluded_ids=excluded_ids,
    #            search_reconciliation_proposition=search_rec_prop,
    #            context=context)

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
