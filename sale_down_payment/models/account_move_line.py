# Copyright 2019-2024 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sale_id = fields.Many2one(
        'sale.order', string='Sale Order', check_company=True,
        domain="[('partner_invoice_id', 'child_of', partner_id), ('state', '!=', 'cancel'), ('invoice_status', '!=', 'invoiced'), ('company_id', '=', company_id)]")

    @api.constrains('sale_id', 'account_id')
    def _sale_id_check(self):
        for line in self:
            if line.sale_id and line.account_internal_type != 'receivable':
                raise ValidationError(_(
                    "The account move line '%s' is linked to sale order '%s' "
                    "but it uses account '%s' which is not a receivable "
                    "account.")
                    % (line.display_name,
                       line.sale_id.display_name,
                       line.account_id.display_name))

    @api.onchange('account_id')
    def sale_advance_payement_account_id_change(self):
        if self.sale_id and self.account_internal_type != 'receivable':
            self.sale_id = False
