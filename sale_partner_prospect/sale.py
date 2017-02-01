# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        vals = {
            'prospect': False,
            'customer': True}
        for order in self:
            msg = _(
                'Validation of sale order %s triggered the conversion '
                'of this partner from prospect to customer.') % order.name
            if order.partner_id.prospect:
                order.partner_id.write(vals)
                order.partner_id.message_post(msg)
            if (
                    order.partner_id.parent_id and
                    order.partner_id.commercial_partner_id.prospect):
                order.partner_id.commercial_partner_id.write(vals)
                order.partner_id.commercial_partner_id.message_post(msg)
        return super(SaleOrder, self).action_confirm()
