# Copyright 2017-2020 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_warn = fields.Selection(tracking=True)
    property_account_position_id = fields.Many2one(tracking=True)
