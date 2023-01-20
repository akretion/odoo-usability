# Copyright 2023 Akretion France (http://www.akretion.com).
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    res_model_name = fields.Char(related='res_model_id.name', string='Document Type')

    def jump_to_record(self):
        self.ensure_one()
        action = {}
        if self.res_id and self.res_model and self.res_name:
            action.update({
                'type': 'ir.actions.act_window',
                'name': self.res_name,
                'res_model': self.res_model,
                'view_mode': 'form',
                'res_id': self.res_id,
                })
        return action
