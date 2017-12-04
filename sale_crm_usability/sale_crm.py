# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        won_stages = self.env['crm.stage'].search(
            [('probability', '=', 100)])
        if won_stages:
            won_stage = won_stages[0]
            for order in self:
                if order.opportunity_id:
                    order.opportunity_id.stage_id = won_stage
                    order.opportunity_id.message_post(_(
                        "Stage automatically updated to <i>%s</i> upon "
                        "confirmation of the quotation <b>%s</b>")
                        % (won_stage.name, order.name))
        return res


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def opportunity_from_quote_get_stage(self):
        '''Designed to be inherited'''
        res = False
        stages = self.env['crm.stage'].search([
            ('probability', '<', 100),
            ('probability', '>', 0),
            ], order='sequence desc', limit=1)
        if stages:
            res = stages
        return res

    @api.model
    def create(self, vals):
        if vals is None:
            vals = {}
        if self._context.get('opportunity_from_quote'):
            stage = self.opportunity_from_quote_get_stage()
            if stage:
                vals['stage_id'] = stage.id
        return super(CrmLead, self).create(vals)
