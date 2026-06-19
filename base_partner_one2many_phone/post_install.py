# Copyright 2017-2023 Akretion France (http://www.akretion.com/)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


def create_partner_phone(env, phone_field, phone_type):
    env.cr.execute(
        'SELECT id, ' + phone_field + ' FROM res_partner WHERE ' +
        phone_field + ' IS NOT null AND ' + phone_field + "!= ''")
    to_create = []
    for partner in env.cr.fetchall():
        to_create.append({
            'partner_id': partner[0],
            'type': phone_type,
            'phone': partner[1],
            })
    return to_create


def create_partner_email(env):
    env.cr.execute(
        "SELECT id, email FROM res_partner WHERE email IS NOT null AND email != ''")
    to_create = []
    for partner in env.cr.fetchall():
        to_create.append({
            'partner_id': partner[0],
            'type': '1_email_primary',
            'email': partner[1],
            })
    return to_create


def migrate_to_partner_phone(env):
    logger.info('start data migration for one2many_phone')
    rppo = env['res.partner.phone']
    to_create = []
    to_create += create_partner_phone(env, 'phone', '3_phone_primary')
    to_create += create_partner_phone(env, 'mobile', '5_mobile_primary')
    to_create += create_partner_email(env)
    # I need to create all at the end for invalidation purposes
    rppo.create(to_create)
    logger.info('end data migration for one2many_phone')
