# Copyright 2017-2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Bank Reconciliation Report",
    "version": "14.0.2.0.0",
    "license": "AGPL-3",
    "author": "Akretion",
    "website": "https://github.com/akretion/odoo-usability",
    "summary": "Bank reconciliation XLSX report",
    "depends": ["account", "report_xlsx"],
    "data": [
        "report/report.xml",
        "wizard/bank_reconciliation_report_wizard_view.xml",
        "views/account_bank_statement.xml",
        "views/account_journal.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}
