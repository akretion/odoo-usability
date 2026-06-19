# Copyright 2018-2024 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from datetime import timedelta


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    already_reversed_warning = fields.Text(compute="_compute_already_reversed_warning")

    @api.depends("move_ids")
    def _compute_already_reversed_warning(self):
        for wizard in self:
            moves = wizard.move_ids or self.env["account.move"].browse(self._context['active_ids'])
            reversed_moves = self.env["account.move"].search([('reversed_entry_id', 'in', moves.ids)])
            # in v18, display_name contains "MISC/2024/0008 (Reversal of: MISC/2024/0007)"
            warning = "\n".join([m.display_name for m in reversed_moves])
            wizard.already_reversed_warning = warning

    # Set default reversal date to original move + 1 day
    # and raise error if original move has already been reversed
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        assert self._context.get('active_model') == 'account.move'
        amo = self.env['account.move']
        moves = amo.browse(self._context['active_ids'])
        if len(moves) == 1 and moves.move_type == 'entry':
            res['date'] = moves.date + timedelta(1)
        return res
