# Copyright 2017-2021 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    probability = fields.Float(tracking=100)
    date_deadline = fields.Date(tracking=110)
    name = fields.Char(tracking=1)
