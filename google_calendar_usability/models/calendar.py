# Copyright 2021 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class Meeting(models.Model):
    _inherit = "calendar.event"

    def unlink(self):
        to_archive = self.filtered(lambda r: r.google_id and r.active)
        if to_archive:
            to_archive.write({"active": False})
        to_unlink = self - to_archive
        super(Meeting, to_unlink).unlink()
