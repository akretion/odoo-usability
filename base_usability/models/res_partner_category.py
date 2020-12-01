# Copyright 2015-2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerCategory(models.Model):
    _inherit = 'res.partner.category'

    name = fields.Char(translate=False)
