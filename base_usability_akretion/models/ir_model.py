# Copyright 2019-2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.depends('name', 'model')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f'{rec.name} ({rec.model})'
