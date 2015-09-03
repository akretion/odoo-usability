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
        afo = self.env['account.fiscalyear']
        # Force 'date_from' to the first day of the company's life
        # in order to get the full picture of the partner's account
        # (we could also do that via a filter by period, but, in this case,
        # account_financial_report_webkit doesn't accept "until_date = today" ;
        # until_date has to be the end date of the last period
        fy_years = afo.search([], order='date_start')
        date_from = fy_years[0].date_start
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
        vals['date_from'] = date_from
        wizard = aoiwo.create(vals)
        data = {'form': {
            'chart_account_id': wizard.chart_account_id.id,
            'filter': vals['filter'],
            'date_from': vals['date_from'],
            'date_to': vals['date_to'],
            'period_to': False,
            'fiscalyear_id': vals['fiscalyear_id'],
            'partner_ids': vals['partner_ids'][0][2],
            'target_move': vals['target_move'],
            }
        }
        action = wizard._print_report(data)
        return action
