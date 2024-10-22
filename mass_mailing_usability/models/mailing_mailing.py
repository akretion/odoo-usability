# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    def action_view_clicked(self):
        action = super().action_view_clicked()
        action["view_mode"] = "tree,form"
        return action
