# Copyright 2021 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    dummy_cal_client_id = fields.Char(
        "Client_id",
        compute="_compute_dummy_gcal_credentials",
        inverse="_inverse_dummy_cal_client_id",
    )
    dummy_cal_client_secret = fields.Char(
        "Client_key",
        compute="_compute_dummy_gcal_credentials",
        inverse="_inverse_dummy_cal_client_secret",
    )

    def _compute_dummy_gcal_credentials(self):
        for rec in self:
            rec.dummy_cal_client_id = ""
            rec.dummy_cal_client_secret = ""

    def _inverse_dummy_cal_client_id(self):
        for rec in self:
            rec.cal_client_id = rec.dummy_cal_client_id

    def _inverse_dummy_cal_client_secret(self):
        for rec in self:
            rec.cal_client_secret = rec.dummy_cal_client_secret
