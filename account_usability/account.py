# Copyright 2015-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.tools import float_compare, float_is_zero
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo import SUPERUSER_ID
import logging

logger = logging.getLogger(__name__)


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
    sale_dates = fields.Char(
        compute="_compute_sales_dates", readonly=True,
        help="This information appears on invoice qweb report "
             "(you may use it for your own report)")

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
                name = u'%s ...' % ', '.join(name.split(', ')[:3])
                # if not enough, hard cut
                if len(name) > 120:
                    name = u'%s ...' % old_re[1][:120]
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
        lines = self.env['account.invoice.line'].search([
            ('invoice_id', 'in', self.ids), ('quantity', '=', 0)])
        lines.unlink()
        return True

    def fix_invoice_attachment_filename(self):
        # This script is designed to fix attachment of invoices
        # badly generated by Odoo v8. I found this problem in Nov 2018 at
        # Encres Dubuit when investigating a bug where Odoo would create a
        # new attachment when printing an old invoice that already had the
        # PDF of the invoice as attachment
        logger.info('START fix customer invoice attachment filename')
        # Run this script as admin to fix problem in all companies
        self = self.sudo()
        attachs = self.env['ir.attachment'].search([
            ('res_model', '=', 'account.invoice'),
            ('res_id', '!=', False),
            ('type', '=', 'binary'),
            ('name', '=like', 'INV%.pdf'),
            ('datas_fname', '=like', 'INV%.pdf.pdf')])
        for attach in attachs:
            inv = self.browse(attach.res_id)
            if inv.type in ('out_invoice', 'out_refund'):
                attach.datas_fname = attach.name
                logger.info(
                    'Fixed field datas_fname of attachment ID %s name %s',
                    attach.id, attach.name)
        logger.info('END fix customer invoice attachment filename')

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
            date_format = self.env["res.lang"]._lang_get(
                lang or "").date_format
            dates = ["%s%s" % (
                     x.name,
                     x.confirmation_date and " (%s)" %
                     # only when confirmation_date display it
                     x.confirmation_date.strftime(date_format) or "")
                     for x in sales]
            inv.sale_dates = ", ".join(dates)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # In the 'account' module, we have related stored field for:
    # company_id, partner_id, currency_id
    invoice_type = fields.Selection(store=True)
    date_invoice = fields.Date(
        related='invoice_id.date_invoice', store=True, readonly=True)
    commercial_partner_id = fields.Many2one(
        related='invoice_id.partner_id.commercial_partner_id',
        store=True, readonly=True, compute_sudo=True)
    state = fields.Selection(
        related='invoice_id.state', store=True, readonly=True,
        string='Invoice State')
    invoice_number = fields.Char(
        related='invoice_id.move_id.name', store=True, readonly=True,
        string='Invoice Number')


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    hide_bank_statement_balance = fields.Boolean(
        string='Hide Bank Statement Balance',
        help="You may want to enable this option when your bank "
        "journal is generated from a bank statement file that "
        "doesn't handle start/end balance (QIF for instance) and "
        "you don't want to enter the start/end balance manually: it "
        "will prevent the display of wrong information in the accounting "
        "dashboard and on bank statements.")

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

    @api.constrains('default_credit_account_id', 'default_debit_account_id')
    def _check_account_type_on_bank_journal(self):
        bank_acc_type = self.env.ref('account.data_account_type_liquidity')
        for jrl in self:
            if jrl.type in ('bank', 'cash'):
                if (
                        jrl.default_debit_account_id and
                        jrl.default_debit_account_id.user_type_id !=
                        bank_acc_type):
                    raise ValidationError(_(
                        "On journal '%s', the default debit account '%s' "
                        "should be configured with Type = 'Bank and Cash'.")
                        % (jrl.display_name,
                           jrl.default_debit_account_id.display_name))
                if (
                        jrl.default_credit_account_id and
                        jrl.default_credit_account_id.user_type_id !=
                        bank_acc_type):
                    raise ValidationError(_(
                        "On journal '%s', the default credit account '%s' "
                        "should be configured with Type = 'Bank and Cash'.")
                        % (jrl.display_name,
                           jrl.default_credit_account_id.display_name))


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.depends('name', 'code')
    def name_get(self):
        if self._context.get('account_account_show_code_only'):
            res = []
            for record in self:
                res.append((record.id, record.code))
            return res
        else:
            return super().name_get()

    # https://github.com/odoo/odoo/issues/23040
    # TODO mig to v12
    def fix_bank_account_types(self):
        aao = self.env['account.account']
        companies = self.env['res.company'].search([])
        if len(companies) > 1 and self.env.user.id != SUPERUSER_ID:
            raise UserError(
                "In multi-company setups, you should run this "
                "script as admin user")
        logger.info("START the script 'fix bank and cash account types'")
        bank_type = self.env.ref('account.data_account_type_liquidity')
        asset_type = self.env.ref('account.data_account_type_current_assets')
        journals = self.env['account.journal'].search(
            [('type', 'in', ('bank', 'cash'))], order='company_id')
        journal_accounts_bank_type = aao
        for journal in journals:
            for account in [
                    journal.default_credit_account_id,
                    journal.default_debit_account_id]:
                if account:
                    if account.user_type_id != bank_type:
                        account.user_type_id = bank_type.id
                        logger.info(
                            'Company %s: Account %s updated to Bank '
                            'and Cash type',
                            account.company_id.display_name, account.code)
                    if account not in journal_accounts_bank_type:
                        journal_accounts_bank_type += account
        accounts = aao.search([
            ('user_type_id', '=', bank_type.id)], order='company_id, code')
        for account in accounts:
            if account not in journal_accounts_bank_type:
                account.user_type_id = asset_type.id
                logger.info(
                    'Company %s: Account %s updated to Current Asset type',
                    account.company_id.display_name, account.code)
        logger.info("END of the script 'fix bank and cash account types'")
        return True

    @api.model
    def create_account_groups(self, level=2, name_prefix=u'Comptes '):
        '''Should be launched by a script. Make sure the account_group module is installed
        (the account_usability module doesn't depend on it currently'''
        assert level >= 1
        assert isinstance(level, int)
        companies = self.env['res.company'].search([])
        if len(companies) > 1:
            logger.info(
                'Multi-company detected: running script create_account_groups '
                'as admin')
            self = self.sudo()
        ago = self.env['account.group']
        groups = ago.search([])
        if groups:
            raise UserError(_("Some account groups already exists"))
        accounts = self.search([])
        struct = {'childs': {}}
        for account in accounts:
            assert len(account.code) > level
            n = 1
            parent = struct
            gparent = False
            while n <= level:
                group_code = account.code[:n]
                if group_code not in parent['childs']:
                    new_group = ago.create({
                        'name': u'%s%s' % (name_prefix or '', group_code),
                        'code_prefix': group_code,
                        'parent_id': gparent and gparent.id or False,
                        })
                    parent['childs'][group_code] = {'obj': new_group, 'childs': {}}
                parent = parent['childs'][group_code]
                gparent = parent['obj']
                n += 1
            account.group_id = gparent.id


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    def name_get(self):
        if self._context.get('analytic_account_show_code_only'):
            res = []
            for record in self:
                res.append((record.id, record.code or record.name))
            return res
        else:
            return super().name_get()

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
    date = fields.Date(copy=False)
    default_account_id = fields.Many2one(
        related='journal_id.default_debit_account_id', readonly=True)
    default_credit = fields.Float(
        compute='_compute_default_credit_debit', readonly=True)
    default_debit = fields.Float(
        compute='_compute_default_credit_debit', readonly=True)

    @api.depends('line_ids.credit', 'line_ids.debit')
    def _compute_default_credit_debit(self):
        for move in self:
            total_debit = total_credit = default_debit = default_credit = 0.0
            for l in move.line_ids:
                total_debit += l.debit
                total_credit += l.credit
            # I could use float_compare, but I don't think it's really needed
            # in this context
            if total_debit > total_credit:
                default_credit = total_debit - total_credit
            else:
                default_debit = total_credit - total_debit
            move.default_credit = default_credit
            move.default_debit = default_debit


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
    account_reconcile = fields.Boolean(
        related='account_id.reconcile', readonly=True)
    full_reconcile_id = fields.Many2one(string='Full Reconcile')
    matched_debit_ids = fields.One2many(string='Partial Reconcile Debit')
    matched_credit_ids = fields.One2many(string='Partial Reconcile Credit')
    reconcile_string = fields.Char(
        compute='_compute_reconcile_string', string='Reconcile', store=True)

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


class AccountPartialReconcile(models.Model):
    _inherit = "account.partial.reconcile"
    _rec_name = "id"

    def name_get(self):
        res = []
        for rec in self:
            # There is no seq for partial rec, so I simulate one with the ID
            # Prefix for full rec: 'A' (upper case)
            # Prefix for partial rec: 'a' (lower case)
            amount_fmt = formatLang(self.env, rec.amount, currency_obj=rec.company_currency_id)
            name = 'a%d (%s)' % (rec.id, amount_fmt)
            res.append((rec.id, name))
        return res


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    start_date = fields.Date(
        compute='_compute_dates', string='Start Date', readonly=True,
        store=True)
    end_date = fields.Date(
        compute='_compute_dates', string='End Date', readonly=True,
        store=True)
    hide_bank_statement_balance = fields.Boolean(
        related='journal_id.hide_bank_statement_balance', readonly=True)

    @api.depends('line_ids.date')
    def _compute_dates(self):
        for st in self:
            dates = [line.date for line in st.line_ids]
            st.start_date = dates and min(dates) or False
            st.end_date = dates and max(dates) or False

    def _balance_check(self):
        for stmt in self:
            if stmt.hide_bank_statement_balance:
                continue
            else:
                super(AccountBankStatement, stmt)._balance_check()
        return True

    @api.depends('name', 'start_date', 'end_date')
    def name_get(self):
        res = []
        for statement in self:
            name = "%s (%s => %s)" % (
                statement.name, statement.start_date, statement.end_date)
            res.append((statement.id, name))
        return res


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
    #    return super().\
    #        get_data_for_reconciliations(
    #            cr, uid, ids, excluded_ids=excluded_ids,
    #            search_reconciliation_proposition=search_rec_prop,
    #            context=context)

    def _prepare_reconciliation_move(self, move_ref):
        vals = super()._prepare_reconciliation_move(move_ref)
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

    def show_account_move(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window'].for_xml_id(
            'account', 'action_move_line_form')
        if self.journal_entry_ids:
            action.update({
                'views': False,
                'view_id': False,
                'view_mode': 'form,tree',
                'res_id': self.journal_entry_ids[0].move_id.id,
                })
            return action
        else:
            raise UserError(_(
                'No journal entry linked to this bank statement line.'))


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    # TODO mig to v12 ?
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


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    @api.depends('code', 'name')
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '[%s] %s' % (rec.code, rec.name)))
        return res


class AccountReconciliation(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    # Add ability to filter by account code in the work interface of the
    # bank statement
    @api.model
    def _domain_move_lines(self, search_str):
        str_domain = super()._domain_move_lines(search_str)
        account_code_domain = [('account_id.code', '=ilike', search_str + '%')]
        str_domain = expression.OR([str_domain, account_code_domain])
        return str_domain

    @api.model
    def _domain_move_lines_for_reconciliation(
            self, st_line, aml_accounts, partner_id,
            excluded_ids=None, search_str=False):
        domain = super()._domain_move_lines_for_reconciliation(
            st_line, aml_accounts, partner_id,
            excluded_ids=excluded_ids, search_str=search_str)
        # We want to replace a domain item by another one
        if ('payment_id', '<>', False) in domain:
            position = domain.index(('payment_id', '<>', False))
            domain[position] = ['journal_id', '=', st_line.journal_id.id]
        return domain


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    transfer_account_id = fields.Many2one(
        related='company_id.transfer_account_id', readonly=False)
