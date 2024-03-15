# Copyright 2019-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    sale_id = fields.Many2one('sale.order', string='Sale Order')

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        line_vals_list = super()._prepare_move_line_default_vals(
            write_off_line_vals=write_off_line_vals)
        # Add to the receivable/payable line
        if (
                self.sale_id and
                len(line_vals_list) >= 2 and
                line_vals_list[1].get('account_id') == self.destination_account_id.id):
            line_vals_list[1]['sale_id'] = self.sale_id.id
        return line_vals_list

    def action_post(self):
        super().action_post()
        for pay in self:
            if pay.sale_id and pay.payment_type == 'inbound':
                pay._sale_down_payment_hook()

    def _sale_down_payment_hook(self):
        # can be used for notifications
        # WAS on account.move.line on v12 ; is on account.payment on v14
        self.ensure_one()
