# Copyright 2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    def action_show_quants(self):
        self.ensure_one()
        action = self.env['stock.quant']._get_quants_action(domain=[('location_id', 'child_of', self.id)])
        return action
