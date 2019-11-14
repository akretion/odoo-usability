# Copyright 2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_id = fields.Many2one('sale.order', string='Sale Order')
    account_internal_type = fields.Selection(
        related='account_id.user_type_id.type', store=True,
        string='Account Internal Type')

    @api.constrains('sale_id', 'account_id')
    def sale_id_check(self):
        for line in self:
            if line.sale_id and line.account_id.internal_type != 'receivable':
                raise ValidationError(_(
                    "The account move line '%s' is linked to sale order '%s' "
                    "but it uses account '%s' which is not a receivable "
                    "account.")
                    % (line.name,
                       line.sale_id.name,
                       line.account_id.display_name))

    @api.onchange('account_id')
    def sale_advance_payement_account_id_change(self):
        if self.sale_id and self.account_id.user_type_id.type != 'receivable':
            self.sale_id = False
