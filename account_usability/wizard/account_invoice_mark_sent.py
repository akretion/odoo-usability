# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models
import logging
logger = logging.getLogger(__name__)


class AccountInvoiceMarkSent(models.TransientModel):
    _name = 'account.invoice.mark.sent'
    _description = 'Mark invoices as sent'

    def run(self):
        assert self.env.context.get('active_model') == 'account.invoice',\
            'Source model must be invoices'
        assert self.env.context.get('active_ids'), 'No invoices selected'
        invoices = self.env['account.invoice'].search([
            ('id', 'in', self.env.context.get('active_ids')),
            ('state', 'in', ('open', 'paid'))])
        invoices.write({'sent': True})
        logger.info('Marking invoices with ID %s as sent', invoices.ids)
        return
