# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    commission_date_range_type_id = fields.Many2one(
        related='company_id.commission_date_range_type_id', readonly=False)
