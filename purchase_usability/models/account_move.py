# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def delete_lines_qty_zero(self):
        # When a user pulls a PO from a supplier invoice, it creates
        # all lines including lines that haven't been received. It can be time-consuming
        # to delete all these lines with qty = 0
        self.ensure_one()
        lines = self.env['account.move.line'].search([
            ('move_id', '=', self.id),
            ('quantity', '=', 0),
            ('display_type', '=', False),
            ])
        lines.unlink()
