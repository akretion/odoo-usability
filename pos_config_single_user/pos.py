# Copyright 2014-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import UserError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    allowed_user_id = fields.Many2one(
        'res.users', string="Allowed User",
        help="If you select a user, only this user will be allowed to start "
        "sessions for this POS", ondelete='restrict')

    def open_session_cb(self, check_coa=True):
        self.ensure_one()
        if (
                self.allowed_user_id and
                self.allowed_user_id != self.env.user):
            raise UserError(_(
                "The POS '%s' can be used only by user '%s'.") % (
                    self.display_name,
                    self.allowed_user_id.display_name))
        return super().open_session_cb(check_coa=check_coa)
