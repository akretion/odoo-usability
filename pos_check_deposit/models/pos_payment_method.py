# Copyright 2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    split_transactions = fields.Boolean(string="Split Transactions")
    identify_customer = fields.Boolean(string='Identify Customer')

    @api.constrains('split_transactions', 'identify_customer')
    def _check_split_transactions_identify_customer(self):
        for method in self:
            if method.identify_customer and not method.split_transactions:
                raise ValidationError(_(
                    "On payment method '%s' the option 'Identify Customer' "
                    "is enabled, so the option 'Split Transactions' must "
                    "be enabled too.") % method.display_name)

    @api.onchange('split_transactions')
    def split_transactions_change(self):
        if not self.split_transactions and self.identify_customer:
            self.identify_customer = False
