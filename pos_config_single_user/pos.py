# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from openerp.exceptions import UserError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    allowed_user_id = fields.Many2one(
        'res.users', string="Allowed User",
        help="If you select a user, only this user will be allowed to start "
        "sessions for this POS", ondelete='restrict')

    @api.multi
    def open_session_cb(self):
        self.ensure_one()
        if (
                self.allowed_user_id and
                self.allowed_user_id != self.env.user):
            raise UserError(_(
                "The POS '%s' can be used only by user '%s'.") % (
                    self.name,
                    self.allowed_user_id.name))
        return super(PosConfig, self).open_session_cb()
