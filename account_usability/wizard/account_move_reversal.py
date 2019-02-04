# Copyright 2018-2019 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    @api.model
    def _default_date(self):
        date = None
        if (
                self._context.get('active_model') == 'account.move' and
                self._context.get('active_id')):
            move = self.env['account.move'].browse(self._context['active_id'])
            date_dt = fields.Date.from_string(move.date) +\
                relativedelta(days=1)
            date = fields.Date.to_string(date_dt)
        return date

    date = fields.Date(default=_default_date)
