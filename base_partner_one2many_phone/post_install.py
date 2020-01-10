# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID
import logging
logger = logging.getLogger(__name__)


def create_partner_phone(cr, phone_field, phone_type):
    cr.execute(
        'SELECT id, ' + phone_field + ' FROM res_partner WHERE ' +
        phone_field + ' IS NOT null')
    to_create = []
    for partner in cr.fetchall():
        to_create.append({
            'partner_id': partner[0],
            'type': phone_type,
            'phone': partner[1],
            })
    return to_create


def create_partner_email(cr):
    cr.execute('SELECT id, email FROM res_partner WHERE email IS NOT null')
    to_create = []
    for partner in cr.fetchall():
        to_create.append({
            'partner_id': partner[0],
            'type': '1_email_primary',
            'email': partner[1],
            })
    return to_create


def migrate_to_partner_phone(cr, registry):
    logger.info('start data migration for one2many_phone')
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        rppo = env['res.partner.phone']
        to_create = []
        to_create += create_partner_phone(cr, 'phone', '3_phone_primary')
        to_create += create_partner_phone(cr, 'mobile', '5_mobile_primary')
        to_create += create_partner_phone(cr, 'fax', '7_fax_primary')
        to_create += create_partner_email(cr)
        # I need to create all at the end for invalidation purposes
        for vals in to_create:
            rppo.create(vals)
            logger.info(
                'partner_phone type %s phone %s email %s created for partner ID %d',
                vals['type'], vals.get('phone'), vals.get('mail'), vals['partner_id'])
    logger.info('end data migration for one2many_phone')
    return
