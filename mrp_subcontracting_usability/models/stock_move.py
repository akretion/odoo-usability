# Copyright 2024 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    subcontracting_production_id = fields.Many2one(
        'mrp.production',
        compute='_compute_subcontracting_production_id',
        )

    def _compute_subcontracting_production_id(self):
        for move in self:
            subcontracting_production_id = False
            if move.is_subcontract and move.move_orig_ids.production_id:
                subcontracting_production_id = move.move_orig_ids.production_id[-1:].id
            move.subcontracting_production_id = subcontracting_production_id
