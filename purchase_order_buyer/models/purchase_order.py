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
        """Update the user_id (buyer)"""
        for rec in self:
            if rec.partner_id and rec.partner_id.user_id:
                user_id = rec.partner_id.user_id.id
            else:
                user_id = self.env.user
            return rec.update({
                'user_id': user_id,
            })
