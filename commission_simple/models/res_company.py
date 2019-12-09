# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    commission_date_range_type_id = fields.Many2one(
        'date.range.type', string='Commission Periodicity')
