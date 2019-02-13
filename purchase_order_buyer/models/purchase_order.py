# -*- coding: utf-8 -*-
# Copyright 2018 Raphael Reverdy https://akretion.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    user_id = fields.Many2one(
        'res.users',
        string='Buyer', index=True,
        track_visibility='onchange',
        default=lambda self: self.env.user)

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        if self.partner_id and self.partner_id.user_id:
            self.user_id = self.partner_id.user_id.id
        else:
            self.user_id = self.env.user
        return res
