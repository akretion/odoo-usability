# Copyright 2017-2019 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_warn = fields.Selection(track_visibility='onchange')
    property_account_position_id = fields.Many2one(
        track_visibility='onchange')
