# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    main_acquirer_id = fields.Many2one(
        'payment.acquirer',
        'Acquirer',
        compute="_compute_main_acquirer",
        store=True)

    @api.depends("transaction_ids.state")
    def _compute_main_acquirer(self):
        for record in self:
            if len(record.transaction_ids.acquirer_id) > 1:
                for state in ["done", "authorized", "pending", "draft", "cancel", "error"]:
                    transaction = record.transaction_ids.filtered(lambda s: s.state == state)
                    if len(transaction.acquirer_id) > 1:
                        transaction.sorted("amount")
                    if transaction:
                        record.main_acquirer_id = transaction[0].acquirer_id
                        break
            else:
                record.main_acquirer_id = record.transaction_ids.acquirer_id

