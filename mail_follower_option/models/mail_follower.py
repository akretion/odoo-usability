# -*- coding: utf-8 -*-

from odoo import models, api


class Followers(models.Model):
    _inherit = 'mail.followers'

    @api.model
    def create(self, vals):
        # Do not implicitly create followers on an object
        model = self.env['ir.model'].search([
            ('model', '=', vals['res_model']),
            ('mail_follower', '=', True),
        ], limit=1)
        if not model:
            return
        return super(Followers, self).create(vals)
