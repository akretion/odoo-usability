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


def migrate_to_partner_phone(cr, registry):
    """This post_install script is required because, when the module
    is installed, Odoo creates the column in the DB and compute the field
    and THEN it loads the file data/res_country_department_data.yml...
    So, when it computes the field on module installation, the
    departments are not available in the DB, so the department_id field
    on res.partner stays null. This post_install script fixes this."""
    logger.info('start data migration for one2many_phone')
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        rppo = env['res.partner.phone']
        to_create = []
        to_create += create_partner_phone(cr, 'phone', '1_home')
        to_create += create_partner_phone(cr, 'mobile', '2_mobile')
        to_create += create_partner_phone(cr, 'fax', '5_office_fax')
        # I need to create all at the end for invalidation purposes
        for vals in to_create:
            rppo.create(vals)
            logger.info(
                'partner_phone type %s phone %s created for partner ID %d',
                vals['type'], vals['phone'], vals['partner_id'])
    logger.info('end data migration for one2many_phone')
    return
