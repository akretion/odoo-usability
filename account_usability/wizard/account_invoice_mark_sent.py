# Copyright 2017-2020 Akretion France (https://akretion.com/en)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models
import logging
logger = logging.getLogger(__name__)


class AccountInvoiceMarkSent(models.TransientModel):
    _name = 'account.invoice.mark.sent'
    _description = 'Mark invoices as sent'

    def run(self):
        assert self.env.context.get('active_model') == 'account.move',\
            'Source model must be invoices'
        assert self.env.context.get('active_ids'), 'No invoices selected'
        invoices = self.env['account.move'].search([
            ('id', 'in', self.env.context.get('active_ids')),
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('state', '=', 'posted')])
        invoices.write({'is_move_sent': True})
        logger.info('Marking invoices with ID %s as sent', invoices.ids)
        return
