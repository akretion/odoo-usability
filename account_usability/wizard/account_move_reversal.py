# Copyright 2018-2020 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    already_reversed_warning = fields.Text(compute="_compute_already_reversed_warning")

    @api.depends("move_ids")
    def _compute_already_reversed_warning(self):
        for wizard in self:
            moves = wizard.move_ids or self.env["account.move"].browse(self._context['active_ids'])
            reversed_moves = self.env["account.move"].search([('reversed_entry_id', 'in', moves.ids)])
            warning = ""
            for already_reversed_move in reversed_moves.reversed_entry_id:
                if warning:
                    warning += "\n"
                reversed_by = " ; ".join(already_reversed_move.reversal_move_id.mapped("display_name"))
                move_detail = _("%s reversed by %s") % (already_reversed_move.display_name, reversed_by)
                warning += move_detail
            wizard.already_reversed_warning = warning or False


    # Set default reversal date to original move + 1 day
    # and raise error if original move has already been reversed
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        assert self._context.get('active_model') == 'account.move'
        amo = self.env['account.move']
        moves = amo.browse(self._context['active_ids'])
        if len(moves) == 1 and moves.move_type not in ('out_invoice', 'in_invoice'):
            res['date'] = moves.date + relativedelta(days=1)
        return res