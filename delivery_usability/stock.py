# Copyright 2018-2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    carrier_id = fields.Many2one(track_visibility='onchange')
    carrier_tracking_ref = fields.Char(track_visibility='onchange')
