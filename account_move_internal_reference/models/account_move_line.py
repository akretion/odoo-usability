# Copyright 2026 Akretion (https://www.akretion.com).
# @author Benoît Guillot <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends(
        "product_id",
        "move_id.ref",
        "move_id.payment_reference",
        "move_id.internal_reference",
    )
    def _compute_name(self):
        """Append the internal reference to the payment term line label.

        The core builds the label of the receivable/payable line from the
        journal entry reference and the payment reference
        (account/models/account_move_line.py:534-542); the internal reference
        is added at the end, with the same logic.
        """
        super()._compute_name()
        for line in self:
            move = line.move_id
            if line.display_type != "payment_term" or not move.internal_reference:
                continue
            if move.internal_reference in (line.name or ""):
                continue
            if line.name:
                line.name = f"{line.name} - {move.internal_reference}"
            else:
                line.name = move.internal_reference
