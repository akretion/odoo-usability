# Copyright 2024 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    @api.depends('name', 'field_description')
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s (%s)' % (rec.field_description, rec.name)))
        return res
