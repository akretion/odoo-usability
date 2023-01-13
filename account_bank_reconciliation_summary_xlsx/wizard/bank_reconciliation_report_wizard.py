# Copyright 2017-2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BankReconciliationReportWizard(models.TransientModel):
    _name = "bank.reconciliation.report.wizard"
    _description = "Bank Reconciliation Report Wizard"
    _check_company_auto = True

    company_id = fields.Many2one(
        'res.company', string='Company',
        ondelete='cascade', required=True,
        default=lambda self: self.env.company)
    date = fields.Date(required=True, default=fields.Date.context_today)
    move_state = fields.Selection(
        [("posted", "Posted Entries"), ("draft_posted", "Draft and Posted Entries")],
        string="Entries",
        required=True,
        default="posted",
    )
    journal_ids = fields.Many2many(
        "account.journal",
        string="Bank Journals",
        domain="[('type', '=', 'bank'), ('company_id', '=', company_id)]",
        required=True,
        check_company=True,
        default=lambda self: self._default_journal_ids(),
    )

    @api.model
    def _default_journal_ids(self):
        journals = self.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("bank_account_id", "!=", False),
                ("company_id", "=", self.env.company.id),
            ]
        )
        return journals
