# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _default_pref_picking_type(self):
        default_in_type = self.env.user.context_default_warehouse_id.in_type_id
        if default_in_type:
            return default_in_type.id
        return self._default_picking_type

    picking_type_id = fields.Many2one(default=_default_pref_picking_type)
