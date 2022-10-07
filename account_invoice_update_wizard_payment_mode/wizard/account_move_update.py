# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import models, fields, api, _


class AccountMoveUpdate(models.TransientModel):
    _inherit = 'account.move.update'

    payment_mode_filter_type_domain = fields.Char(
        related='invoice_id.payment_mode_filter_type_domain')
    partner_bank_filter_type_domain = fields.Many2one(
        related='invoice_id.partner_bank_filter_type_domain')
    bank_account_required = fields.Boolean(
        related='invoice_id.bank_account_required')
    payment_mode_id = fields.Many2one("account.payment.mode")

    @api.model
    def _m2o_fields2update(self):
        m2o_list = super()._m2o_fields2update()
        m2o_list.append('payment_mode_id')
        return m2o_list
