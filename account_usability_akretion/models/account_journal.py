# Copyright 2015-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    hide_bank_statement_balance = fields.Boolean(
        string='Hide and Disable Bank Statement Balance', default=True,
        help="When this option is enabled, the start and end balance is "
        "not displayed on the bank statement form view, and the check of "
        "the end balance vs the real end balance is disabled. When you enable "
        "this option, you process the statement lines without considering "
        "the start/end balance and you regularly check the accounting balance "
        "of the bank account vs the amount of your bank account."
        )
    company_currency_id = fields.Many2one(
        related="company_id.currency_id", string="Company Currency", store=True)
    inbound_payment_amount_str = fields.Char(compute="_compute_dashboard_payment_amounts", string="Inbound Payments Amount")
    outbound_payment_amount_str = fields.Char(compute="_compute_dashboard_payment_amounts", string="Outbound Payments Amount")

    @api.depends('name', 'currency_id', 'company_id', 'code')
    @api.depends_context('journal_show_code_only')
    def _compute_display_name(self):
        if self._context.get('journal_show_code_only'):
            for journal in self:
                journal.display_name = journal.code
        else:
            for journal in self:
                name = f"[{journal.code}] {journal.name}"
                if (
                        journal.currency_id and
                        journal.currency_id != journal.company_id.currency_id):
                    name = f"{name} ({journal.currency_id.name})"
                journal.display_name = name

    def _compute_dashboard_payment_amounts(self):
        for journal in self:
            in_amt = out_amt = False
            if journal.type in ("bank", "cash", "credit"):
                company_id = journal.company_id.id
                base_domain = [
                    ('display_type', 'not in', ('line_section', 'line_note')),
                    ('parent_state', '=', 'posted'),
                    ('journal_id', '=', journal.id),
                    ('company_id', '=', company_id),
                    '|', ('matching_number', '=', False), ('matching_number', '=like', 'P%')]
                comp_cur = journal.company_currency_id
                inbound_account_ids, outbound_account_ids = journal._get_inbound_outbound_payment_account_ids()
                if inbound_account_ids:
                    in_rg_res = self.env['account.move.line']._read_group(
                       domain=base_domain + [('account_id', 'in', tuple(inbound_account_ids))],
                        aggregates=['balance:sum'],
                    )
                    in_amt = in_rg_res and in_rg_res[0][0]
                if outbound_account_ids:
                    out_rg_res = self.env['account.move.line']._read_group(
                       domain=base_domain + [('account_id', 'in', tuple(outbound_account_ids))],
                        aggregates=['balance:sum'],
                    )
                    out_amt = out_rg_res and out_rg_res[0][0] * -1
            journal.inbound_payment_amount_str = in_amt and comp_cur.format(in_amt) or False
            journal.outbound_payment_amount_str = out_amt and comp_cur.format(out_amt) or False

    def _get_inbound_outbound_payment_account_ids(self):
        self.ensure_one()
        inbound_account_ids = set()
        outbound_account_ids = set()
        method_lines = self.env['account.payment.method.line'].search_read([
            ('journal_id', '=', self.id),
            ('payment_account_id', '!=', False)
            ], ['payment_account_id', 'payment_type'])
        for method_line in method_lines:
            if method_line['payment_type'] == "inbound" and method_line['payment_account_id']:
                inbound_account_ids.add(method_line['payment_account_id'][0])
            elif method_line['payment_type'] == "outbound" and method_line['payment_account_id']:
                outbound_account_ids.add(method_line['payment_account_id'][0])
        return list(inbound_account_ids), list(outbound_account_ids)

    def dashboard_open_inbound_payment_accounts(self):
        self.ensure_one()
        return self._dashboard_open_payment_accounts('inbound')

    def dashboard_open_outbound_payment_accounts(self):
        self.ensure_one()
        return self._dashboard_open_payment_accounts('outbound')

    def _dashboard_open_payment_accounts(self, payment_type):
        self.ensure_one()
        assert payment_type in ('inbound', 'outbound')
        action = False
        inbound_account_ids, outbound_account_ids = self._get_inbound_outbound_payment_account_ids()
        account_ids = payment_type == "inbound" and inbound_account_ids or outbound_account_ids
        if account_ids:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "account.action_account_moves_all")
            action['domain'] = [
                ('account_id', 'in', account_ids),
                ('display_type', 'not in', ('line_section', 'line_note')),
                ('parent_state', '=', 'posted'),
                ('company_id', '=', self.company_id.id),
                ]
            action['context'] = {
                'search_default_reconcilable_account': True, 'search_default_journal_id': self.id,
                }
        return action
