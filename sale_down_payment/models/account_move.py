# Copyright 2023-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _post(self, soft=True):
        res = super()._post(soft=soft)
        amlo = self.env['account.move.line']
        for move in self:
            if move.state == 'posted' and move.move_type == 'out_invoice':
                sales = move.invoice_line_ids.sale_line_ids.order_id
                if sales:
                    mlines = amlo.search([('sale_id', 'in', sales.ids)])
                    if mlines:
                        mlines_to_reconcile = move.line_ids.filtered(
                            lambda line: line.account_id ==
                            move.commercial_partner_id.property_account_receivable_id)
                        mlines_to_reconcile |= mlines
                        mlines_to_reconcile.remove_move_reconcile()
                        mlines_to_reconcile.reconcile()
        return res
