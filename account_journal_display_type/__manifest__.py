# Copyright 2024 Akretion (https://www.akretion.com).
# @author Matthieu SAISON <matthieu.saison@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Journal Display Type",
    "summary": "Account Journal type for payment",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Accounting",
    "website": "https://github.com/OCA/account-financial-tools",
    "author": "Akretion, " "Odoo Community Association (OCA)",
    "maintainers": ["matthieu_saison"],
    "license": "AGPL-3",
    "depends": ["account", "account_statement_completion_label_simple"],
    "data": ["views/account_journal_view.xml"],
    "post_init_hook": "post_init_hook",
}
