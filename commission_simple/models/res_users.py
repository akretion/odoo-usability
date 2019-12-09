# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    commission_profile_id = fields.Many2one(
        'commission.profile', string='Commission Profile',
        company_dependant=True)
