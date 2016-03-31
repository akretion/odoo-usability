# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from openerp import models, fields, api, _
from openerp.exceptions import Warning as UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lead_id = fields.Many2one(
        'crm.lead', string='Opportunity')

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        won_stage = self.env.ref('crm.stage_lead6')
        for order in self:
            if order.lead_id:
                order.lead_id.stage_id = won_stage
                order.lead_id.message_post(_(
                    "Stage automatically updated to <i>Won</i> upon "
                    "confirmation of the quotation <b>%s</b>" % order.name))
        return res


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sale_ids = fields.One2many(
        'sale.order', 'lead_id', string='Quotations', readonly=True)

    @api.multi
    def view_sale_orders(self):
        self.ensure_one()
        if self.sale_ids:
            action = {
                'name': _('Quotations'),
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'target': 'current',
                'context':
                "{'default_partner_id': %s, 'default_lead_id': %s}" % (
                    self.partner_id.id or False, self[0].id),
                }
            if len(self.sale_ids) == 1:
                action.update({
                    'view_mode': 'form,tree,calendar,graph',
                    'res_id': self.sale_ids[0].id,
                    })
            else:
                action.update({
                    'view_mode': 'tree,form,calendar,graph',
                    'domain': "[('id', 'in', %s)]" % self.sale_ids.ids,
                    })
            return action
        else:
            raise UserError(_(
                'There are no quotations linked to this opportunity'))
