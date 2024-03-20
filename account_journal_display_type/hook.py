from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    journal_ids = env["account.journal"].search([])
    for journal in journal_ids:
        journal.display_type = journal.type
