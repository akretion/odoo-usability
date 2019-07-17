# Copyright 2014-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.model_cr
    def init(self):
        '''Activate 'avoid_quick_create' on all existing models'''
        self._cr.execute(
            "UPDATE ir_model SET avoid_quick_create=true "
            "WHERE avoid_quick_create is not true")
        return True

    avoid_quick_create = fields.Boolean(default=True)
