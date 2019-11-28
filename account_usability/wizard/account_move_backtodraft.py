# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, _
from odoo.exceptions import UserError


class AccountMoveBacktodraft(models.TransientModel):
    _name = 'account.move.backtodraft'
    _description = 'Account Move Unpost'

    def backtodraft(self):
        assert self._context.get('active_model') == 'account.move'
        amo = self.env['account.move']
        moves = amo.browse(self._context.get('active_ids'))
        moves_backtodraft = moves.filtered(lambda x: x.state == 'posted')
        if not moves_backtodraft:
            raise UserError(_(
                'There is no journal items in posted state to unpost.'))
        moves_backtodraft.button_cancel()
        return True
