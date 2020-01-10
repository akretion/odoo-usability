# -*- coding: utf-8 -*-
# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID

oldtype2label = {
    '1_home': 'Ancien type : Maison',
#    '2_mobile': 'Ancien type : Portable',
    '3_office': 'Ancien type : Bureau',
    '4_home_fax': 'Ancien type : Fax maison',
    '5_office_fax': 'Ancien type : Fax bureau',
    '6_phone_fax_home': u'Ancien type : Tél/fax maison',
    '7_other': 'Ancien type : Autre',
    }


def migrate(cr, version):
    if not version:
        return

    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        rppo = env['res.partner.phone']

        wdict = {}  # key = partnerID, values = {id: {'type': '1_home', 'phone': '+33'}}
        for rec in rppo.search_read([('type', '!=', False)], ['type', 'phone', 'partner_id', 'note']):
            if rec['partner_id'][0] not in wdict:
                wdict[rec['partner_id'][0]] = {}
            wdict[rec['partner_id'][0]][rec['id']] = rec

        # first pass for primary phone
        for partner_id, xdict in wdict.items():
            mig_phone_entries(cr, xdict, '3_phone_primary', '4_phone_secondary', ['1_home', '6_phone_fax_home', '3_office', '7_other'])
            mig_phone_entries(cr, xdict, '5_mobile_primary', '6_mobile_secondary', ['2_mobile'])
            mig_phone_entries(cr, xdict, '7_fax_primary', '8_fax_secondary', ['4_home_fax', '5_office_fax'])
        cr.execute('select id, email from res_partner where email is not null order by id')
        for partner in cr.dictfetchall():
            print('partner_id=', partner['id'])
            old_email = partner['email'].strip()
            if old_email:
                email_split = old_email.split(',')
                clean_email_split = [x.strip() for x in email_split if x.strip()]
                # primary:
                email_primary = clean_email_split.pop(0)
                rppo.create({
                    'type': '1_email_primary',
                    'partner_id': partner['id'],
                    'email': email_primary,
                    })
                cr.execute('UPDATE res_partner set email=%s where id=%s', (email_primary, partner['id']))
                for email_sec in clean_email_split:
                    email_sec = email_sec.strip()
                    if email_sec:
                        rppo.create({
                            'type': '2_email_secondary',
                            'partner_id': partner['id'],
                            'email': email_sec.strip(),
                            })


def mig_phone_entries(cr, xdict, new_type_primary, new_type_secondary, old_type_list):
    zdict = {}
    for phone_id, values in xdict.items():
        if values['type'] in old_type_list:
            zdict[phone_id] = values
    if zdict:
        values_sorted = sorted(zdict.values(), key=lambda x: x['type'])
        primary_phone_val = values_sorted[0]
        cr.execute("""UPDATE res_partner_phone SET type=%s WHERE id=%s""", (new_type_primary, primary_phone_val['id']))
        if not primary_phone_val.get('note') and oldtype2label.get(primary_phone_val['type']):
            cr.execute("""UPDATE res_partner_phone SET note=%s WHERE id=%s""", (oldtype2label[primary_phone_val['type']], primary_phone_val['id']))

        zdict.pop(primary_phone_val['id'])
    for secondary_phone_val in zdict.values():
        cr.execute("""UPDATE res_partner_phone SET type=%s WHERE id=%s""", (new_type_secondary, secondary_phone_val['id']))
        if not secondary_phone_val.get('note') and oldtype2label.get(secondary_phone_val['type']):
            cr.execute("""UPDATE res_partner_phone SET note=%s WHERE id=%s""", (oldtype2label[secondary_phone_val['type']], secondary_phone_val['id']))
