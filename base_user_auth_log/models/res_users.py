# -*- coding: utf-8 -*-
# Copyright 2017-2018 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, registry, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    auth_log_ids = fields.One2many(
        'res.users.auth.log', 'user_id', string='Authentication Logs')

    @classmethod
    def _login(cls, db, login, password):
        user_id = super(ResUsers, cls)._login(db, login, password)
        with registry(db).cursor() as cr:
            if user_id:
                result = 'success'
                user_log_id = user_id
            else:
                # To write a null value, psycopg2 wants None
                user_log_id = None
                result = 'failure'
                cr.execute(
                    "SELECT id FROM res_users WHERE login=%s", (login, ))
                user_select = cr.fetchall()
                if user_select:
                    user_log_id = user_select[0][0]

            cr.execute("""
                INSERT INTO res_users_auth_log (
                    create_uid,
                    create_date,
                    date,
                    login,
                    result,
                    user_id
                    ) VALUES (
                    %s, NOW() AT TIME ZONE 'UTC', NOW() AT TIME ZONE 'UTC',
                    %s, %s, %s)""", (SUPERUSER_ID, login, result, user_log_id))
            logger.info('Auth log created for login %s type %s', login, result)
        return user_id
