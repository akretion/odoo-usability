# Copyright 2018-2020 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    # Set default reversal date to original move + 1 day
    # and raise error if original move has already been reversed
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        assert self._context.get('active_model') == 'account.move'
        amo = self.env['account.move']
        moves = amo.browse(self._context['active_ids'])
        if len(moves) == 1:
            res['date'] = moves.date + relativedelta(days=1)
        reversed_move = amo.search([('reversed_entry_id', 'in', moves.ids)], limit=1)
        if reversed_move:
            raise UserError(_(
                "Move '%s' has already been reversed by move '%s'.") % (
                    reversed_move.reversed_entry_id.display_name,
                    reversed_move.display_name))
        return res
