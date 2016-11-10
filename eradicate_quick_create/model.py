# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class IrModel(models.Model):
    _inherit = 'ir.model'

    def init(self):
        '''Activate 'avoid_quick_create' on all existing models'''
        self._cr.execute(
            "UPDATE ir_model SET avoid_quick_create=true "
            "WHERE avoid_quick_create is not true")
        return True

    avoid_quick_create = fields.Boolean(default=True)
