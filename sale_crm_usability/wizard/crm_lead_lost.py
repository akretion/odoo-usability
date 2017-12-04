# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api, _


class CrmLeadLost(models.TransientModel):
    _inherit = 'crm.lead.lost'

    cancel_quotes = fields.Boolean(
        string='Cancel Related Quotations', default=True)

    @api.multi
    def action_lost_reason_apply(self):
        assert self._context.get('active_model') == 'crm.lead', 'wrong model'
        leads = self.env['crm.lead'].browse(self._context.get('active_ids'))
        if self.cancel_quotes and leads:
            quotes = self.env['sale.order'].search([
                ('opportunity_id', 'in', leads.ids),
                ('state', 'in', ('draft', 'sent')),
                ])
            if quotes:
                quotes.action_cancel()
                quotes.message_post(_(
                    "Quotation automatically cancelled upon marking "
                    "the related opportunity as lost."))
        return super(CrmLeadLost, self).action_lost_reason_apply()
