# Copyright 2015-2019 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(track_visibility='onchange')
    incoterm = fields.Many2one(track_visibility='onchange')
