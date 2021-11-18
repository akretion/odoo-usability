# Copyright 2021 Akretion France (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import fields, models


class CrmTag(models.Model):
    _inherit = "crm.tag"

    name = fields.Char(translate=False)
