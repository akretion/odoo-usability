# Copyright 2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def action_invoice_open(self):
        res = super().action_invoice_open()
        amlo = self.env['account.move.line']
        for inv in self:
            if inv.state == 'open' and inv.type == 'out_invoice':
                sales = inv.invoice_line_ids.mapped('sale_line_ids').\
                    mapped('order_id')
                if sales:
                    mlines = amlo.search([('sale_id', 'in', sales.ids)])
                    if mlines:
                        receivable_lines = inv.move_id.mapped('line_ids').filtered(
                            lambda l: l.account_id == inv.account_id)
                        mlines |= receivable_lines
                        mlines.remove_move_reconcile()
                        mlines.reconcile()
        return res
