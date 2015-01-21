# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Statement Operation Multi-company module for Odoo
#    Copyright (C) 2015 Akretion (http://www.akretion.com)
#    @author Alexis de Lattre <alexis.delattre@akretion.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountStatementOperationTemplate(models.Model):
    _inherit = 'account.statement.operation.template'

    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env['res.company']._company_default_get(
            'account.statement.operation.template'))

    @api.one
    @api.constrains('account_id', 'company_id')
    def _check_company(self):
        if (
                self.account_id
                and self.company_id
                and self.account_id.company_id != self.company_id):
            raise ValidationError(
                _("The button %s is attached to the company %s but has an "
                    "account in the company %s")
                % (self.name, self.company_id.name,
                    self.account_id.company_id.name))
