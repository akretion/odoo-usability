# Copyright 2018-2021 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    carrier_id = fields.Many2one(tracking=True)
    carrier_tracking_ref = fields.Char(tracking=True)
