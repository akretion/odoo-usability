# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

def migrate(cr, version):
    if not version:
        return

    # cf the inherit of action_number() of account.invoice
    # in account_usability/account.py
    cr.execute(
        "UPDATE account_move_line SET name=account_move.name "
        "FROM account_move WHERE account_move_line.move_id = account_move.id "
        "AND account_move_line.name='/' "
        "AND account_move_line.journal_id in "
        "(SELECT id FROM account_journal WHERE type in ('purchase', 'purchase_refund'))")
