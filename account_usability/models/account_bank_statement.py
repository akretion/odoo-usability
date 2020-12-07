# Copyright 2015-2020 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.tools.misc import format_date


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

    def _check_balance_end_real_same_as_computed(self):
        for stmt in self:
            if stmt.hide_bank_statement_balance:
                continue
            else:
                super(AccountBankStatement, stmt)._check_balance_end_real_same_as_computed()
        return True

    @api.depends('name', 'start_date', 'end_date')
    def name_get(self):
        res = []
        for statement in self:
            name = "%s (%s => %s)" % (
                statement.name,
                statement.start_date and format_date(self.env, statement.start_date) or '',
                statement.end_date and format_date(self.env, statement.end_date) or '')
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

#    def _prepare_reconciliation_move(self, move_ref):
#        vals = super()._prepare_reconciliation_move(move_ref)
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
#        vals['ref'] = False
#        return vals

    def show_account_move(self):
        self.ensure_one()
        action = self.env.ref('account.action_move_line_form').read()[0]
        # Note: this action is on account.move, not account.move.line !
        if self.journal_entry_ids:
            action.update({
                'views': False,
                'view_id': False,
                'view_mode': 'form,tree',
                'res_id': self.move_id.id,
                })
            return action
        else:
            raise UserError(_(
                'No journal entry linked to this bank statement line.'))


#class AccountFiscalPosition(models.Model):
#    _inherit = 'account.fiscal.position'

    # TODO mig to v14 ?
#    @api.model
#    def get_fiscal_position_no_partner(
#            self, company_id=None, vat_subjected=False, country_id=None):
#        '''This method is inspired by the method get_fiscal_position()
#        in odoo/addons/account/partner.py : it uses the same algo
#        but without a real partner.
#        Returns a recordset of fiscal position, or False'''
#        domains = [[
#            ('auto_apply', '=', True),
#            ('vat_required', '=', vat_subjected),
#            ('company_id', '=', company_id)]]
#        if vat_subjected:
#            domains += [[
#                ('auto_apply', '=', True),
#                ('vat_required', '=', False),
#                ('company_id', '=', company_id)]]

#        for domain in domains:
#            if country_id:
#                fps = self.search(
#                    domain + [('country_id', '=', country_id)], limit=1)
#                if fps:
#                    return fps[0]

#                fps = self.search(
#                    domain +
#                    [('country_group_id.country_ids', '=', country_id)],
#                    limit=1)
#                if fps:
#                    return fps[0]

#            fps = self.search(
#                domain +
#                [('country_id', '=', None), ('country_group_id', '=', None)],
#                limit=1)
#            if fps:
#                return fps[0]
#        return False


#class AccountReconcileModel(models.Model):
#    _inherit = 'account.reconcile.model'

#    @api.onchange('name')
#    def onchange_name(self):
        # Do NOT copy by default name on label
        # Because it's much better to have the bank statement line label as
        # label of the counter-part move line, then the label of the button
#        assert True  # Stupid line of code just to have something...

