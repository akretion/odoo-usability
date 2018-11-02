# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.model
    def _default_pref_picking_type(self):
        default_manu_type = self.env.user.context_default_warehouse_id.\
            manu_type_id
        if default_manu_type:
            return default_manu_type.id
        return self._get_default_picking_type()

    # No need to inherit the default value of location_src_id and
    # location_dest_id because it is immediately over-ridden
    # by the onchange of picking_type_id
    picking_type_id = fields.Many2one(default=_default_pref_picking_type)
