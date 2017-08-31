# -*- coding: utf-8 -*-
# © 2014-2016 Abbaye du Barroux (http://www.barroux.org)
# © 2016 Akretion (http://www.akretion.com>)
# @author: Frère Bernard <informatique@barroux.org>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.addons.base_phone.fields import Phone, Fax
import phonenumbers


class ResPartnerPhone(models.Model):
    _name = 'res.partner.phone'
    _order = 'partner_id, type'
    _phone_name_sequence = 8

    partner_id = fields.Many2one('res.partner', string='Related Partner')
    type = fields.Selection([
        ('1_home', 'Home'),
        ('2_mobile', 'Mobile'),
        ('3_office', 'Office'),
        ('4_home_fax', 'Home Fax'),
        ('5_office_fax', 'Office Fax'),
        ('6_phone_fax_home', 'Phone/fax Home'),
        ('7_other', 'Other')],
        string='Phone Type', required=True)
    phone = Phone('Phone', required=True, partner_field='partner_id')
    note = fields.Char('Note')

    def name_get(self):
        res = []
        for pphone in self:
            if pphone.partner_id:
                if self._context.get('callerid'):
                    name = pphone.partner_id.name_get()[0][1]
                else:
                    name = u'%s (%s)' % (pphone.phone, pphone.partner_id.name)
            else:
                name = pphone.phone
            res.append((pphone.id, name))
        return res


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def convert_from_international_to_e164(self, phone_num):
        res = False
        try:
            res_parse = phonenumbers.parse(phone_num)
            res = phonenumbers.format_number(
                res_parse, phonenumbers.PhoneNumberFormat.E164)
        except:
            pass
        return res
    # without this convert, we would have in DB:
    # E.164 format in res_partner_phone table
    # phonenumbers.PhoneNumberFormat.INTERNATIONAL in res_partner
    # TODO bug: but even with this, it doesn't work, the format
    # is stored in international format in res_partner
    # => I'll try to find the reason later

    @api.multi
    @api.depends('phone_ids.phone', 'phone_ids.type')
    def _compute_partner_phone(self):
        for partner in self:
            phone = mobile = fax = False
            for partner_phone in partner.phone_ids:
                num_e164 = self.convert_from_international_to_e164(
                    partner_phone.phone)
                if num_e164:
                    if partner_phone.type == '2_mobile':
                        mobile = num_e164
                    elif partner_phone.type in ('5_office_fax', '4_home_fax'):
                        fax = num_e164
                    else:
                        phone = num_e164
            partner.phone = phone
            partner.mobile = mobile
            partner.fax = fax

    phone_ids = fields.One2many(
        'res.partner.phone', 'partner_id', string='Phones')
    phone = Phone(
        compute='_compute_partner_phone', store=True, readonly=True)
    mobile = Phone(
        compute='_compute_partner_phone', store=True, readonly=True)
    fax = Fax(
        compute='_compute_partner_phone', store=True, readonly=True)
