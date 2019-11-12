# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountBankStatementSale(models.TransientModel):
    _name = 'account.bank.statement.sale'
    _description = 'Account Bank Statement Sale'

    statement_id = fields.Many2one('account.bank.statement', readonly=True)
    line_ids = fields.One2many(
        'account.bank.statement.sale.line', 'wizard_id', string='Lines')

    @api.model
    def _prepare_line(self, move_line):
        vals = {
            'move_line_id': move_line.id,
            'sale_id': move_line.sale_id.id or False,
            'date': move_line.date,
            'credit': move_line.credit,
            'partner_id': move_line.partner_id.id,
            'account_id': move_line.account_id.id,
            'name': move_line.name,
            'company_currency_id': move_line.company_currency_id.id,
            }
        return vals

    @api.model
    def default_get(self, fields_list):
        res = super(AccountBankStatementSale, self).default_get(fields_list)
        assert self._context.get('active_model') == 'account.bank.statement'
        statement_id = self._context.get('active_id')
        statement = self.env['account.bank.statement'].browse(statement_id)
        res.update({
            'line_ids': [],
            'statement_id': statement_id,
            })
        for st_line in statement.line_ids:
            if (
                    st_line.amount > 0 and
                    st_line.partner_id and
                    st_line.journal_entry_ids):
                for line in st_line.journal_entry_ids:
                    if (
                            line.account_id.user_type_id.type == 'receivable'
                            and
                            line.partner_id and
                            not line.full_reconcile_id and
                            not line.matched_debit_ids and
                            not line.matched_credit_ids):
                        lvals = self._prepare_line(line)
                        res['line_ids'].append((0, 0, lvals))
        if not res['line_ids']:
            raise UserError(_(
                "The bank statement '%s' doesn't contain any processed line "
                "with a positive amount which is not reconciled.")
                % statement.display_name)
        return res

    def validate(self):
        self.ensure_one()
        for line in self.line_ids:
            if line.move_line_id.sale_id != line.sale_id:
                line.move_line_id.sale_id = line.sale_id.id


class AccountBankStatementSaleLine(models.TransientModel):
    _name = 'account.bank.statement.sale.line'
    _description = 'Account Bank Statement Sale Lines'

    wizard_id = fields.Many2one(
        'account.bank.statement.sale', ondelete='cascade')
    move_line_id = fields.Many2one(
        'account.move.line', string='Move Line', required=True)
    date = fields.Date(related='move_line_id.date')
    credit = fields.Monetary(
        related='move_line_id.credit', currency_field='company_currency_id')
    partner_id = fields.Many2one(related='move_line_id.partner_id')
    account_id = fields.Many2one(related='move_line_id.account_id')
    name = fields.Char(related='move_line_id.name')
    company_currency_id = fields.Many2one(
        related='move_line_id.company_currency_id')
    sale_id = fields.Many2one('sale.order', string='Sale Order')
