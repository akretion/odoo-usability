# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account Direct Debit Autogenerate module for Odoo
#    Copyright (C) 2015 Akretion (www.akretion.com)
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

from openerp import models, api, _
from openerp.exceptions import Warning
import logging

logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _prepare_payment_order(self, invoice):
        vals = {
            'mode': invoice.payment_mode_id.id,
            'payment_order_type': 'debit',
            }
        return vals

    @api.model
    def _prepare_payment_line(self, move_line, payment_order):
        assert move_line.invoice, 'The move line must be linked to an invoice'
        if not move_line.invoice.mandate_id:
            raise Warning(
                _('Missing Mandate on Invoice %s') % move_line.invoice.number)
        vals = {
            'order_id': payment_order.id,
            'move_line_id': move_line.id,
            'partner_id': move_line.partner_id.id,
            'amount_currency': move_line.amount_to_receive,
            'communication': move_line.invoice.number.replace('/', ''),
            'state': 'structured',
            'date': move_line.date_maturity,
            'currency': move_line.invoice.currency_id.id,
            'mandate_id': move_line.invoice.mandate_id.id,
            'bank_id': move_line.invoice.mandate_id.partner_bank_id.id,
            }
        return vals

    @api.multi
    def invoice_validate(self):
        '''Create Direct debit payment order on invoice validation or update
        an existing draft Direct Debit pay order'''
        res = super(AccountInvoice, self).invoice_validate()
        poo = self.env['payment.order']
        plo = self.env['payment.line']
        for invoice in self:
            if (
                    invoice.type == 'out_invoice'
                    and invoice.payment_mode_id
                    and invoice.payment_mode_id.type
                    and invoice.payment_mode_id.type.code
                    and invoice.payment_mode_id.type.code.
                    startswith('pain.008.001.')):
                payorders = poo.search([
                    ('state', '=', 'draft'),
                    ('payment_order_type', '=', 'debit'),
                    ('mode', '=', invoice.payment_mode_id.id),
                    # mode is attached to company
                    ])
                if payorders:
                    payorder = payorders[0]
                    payorder_type = _('existing')
                else:
                    payorder_vals = self._prepare_payment_order(invoice)
                    payorder = poo.create(payorder_vals)
                    payorder_type = _('new')
                    logger.info(
                        'New Direct Debit Order created %s'
                        % payorder.reference)
                move_lines = [
                    line for line in invoice.move_id.line_id
                    if line.account_id == invoice.account_id]
                for move_line in move_lines:
                    if not invoice.mandate_id:
                        raise Warning(
                            _("Missing Mandate on invoice %s")
                            % invoice.number)
                    # add payment line
                    pl_vals = self._prepare_payment_line(move_line, payorder)
                    pl = plo.create(pl_vals)
                    invoice.message_post(
                        _("A new payment line %s has been automatically "
                            "created on the %s direct debit order %s")
                        % (pl.name, payorder_type, payorder.reference))
        return res
