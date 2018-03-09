# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields_list):
        res = super(ResUsers, self).default_get(fields_list)
        # For a new partner auto-created when you create a new user, we prefer
        # customer=False and supplier=True by default
        res.update({
            'customer': False,
            'supplier': True,
            })
        return res
