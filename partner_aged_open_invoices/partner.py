# -*- encoding: utf-8 -*-
##############################################################################
#
#    Partner Aged Open Invoices module for Odoo
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

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('credit', 'debit')
    def _compute_balance(self):
        self.balance = self.credit - self.debit

    balance = fields.Float(
        compute='_compute_balance', readonly=True,
        digits=dp.get_precision('Account'), string="Account Balance")

    @api.multi
    def open_aged_open_invoices_report(self):
        aoiwo = self.env['aged.open.invoices.webkit']
        fy_id = aoiwo._get_fiscalyear()
        filter_change = aoiwo.onchange_filter(
            filter='filter_date', fiscalyear_id=fy_id)
        vals = {
            'fiscalyear_id': fy_id,
            'filter': 'filter_date',
            'partner_ids': [(6, 0, [self.commercial_partner_id.id])],
            'target_move': 'all',
            }
        vals.update(filter_change['value'])
        wizard = self.env['aged.open.invoices.webkit'].create(vals)
        data = {'form': {
            'chart_account_id': wizard.chart_account_id.id,
            'filter': 'filter_date',
            'date_from': vals['date_from'],
            'date_to': vals['date_to'],
            'period_to': False,
            'fiscalyear_id': fy_id,
            'partner_ids': [self.commercial_partner_id.id],
            'target_move': 'all',
            }
        }
        action = wizard._print_report(data)
        return action
