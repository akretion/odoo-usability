# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, SUPERUSER_ID, _
from odoo.exceptions import UserError
import logging
logger = logging.getLogger(__name__)


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

    @api.model
    def _script_partners_linked_to_users_no_company(self):
        if self.env.user.id != SUPERUSER_ID:
            self = self.sudo()
        logger.info(
            'START to set company_id=False on partners related to users')
        users = self.search(
            ['|', ('active', '=', True), ('active', '=', False)])
        for user in users:
            if user.partner_id.company_id:
                user.partner_id.company_id = False
                logger.info(
                    'Wrote company_id=False on user %s ID %d',
                    user.login, user.id)
        logger.info(
            'END setting company_id=False on partners related to users')
        return True
