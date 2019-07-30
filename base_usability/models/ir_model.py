# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.depends('name', 'model')
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s (%s)' % (rec.name, rec.model)))
        return res
