# -*- coding: utf-8 -*-
# © 2014-2016 Abbaye du Barroux (http://www.barroux.org)
# © 2016 Akretion (http://www.akretion.com>)
# @author: Frère Bernard <informatique@barroux.org>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.addons.base_phone.fields import Phone, Fax

EMAIL_TYPES = ('1_email_primary', '2_email_secondary')
PHONE_TYPES = ('3_phone_primary', '4_phone_secondary', '5_mobile_primary', '6_mobile_secondary', '7_fax_primary', '8_fax_secondary')


class ResPartnerPhone(models.Model):
    _name = 'res.partner.phone'
    _order = 'partner_id, type'
    _phone_name_sequence = 8

    partner_id = fields.Many2one(
        'res.partner', string='Related Partner', index=True, ondelete='cascade')
    type = fields.Selection([
        ('1_email_primary', 'Primary E-mail'),
        ('2_email_secondary', 'Secondary E-mail'),
        ('3_phone_primary', 'Primary Phone'),
        ('4_phone_secondary', 'Secondary Phone'),
        ('5_mobile_primary', 'Primary Mobile'),
        ('6_mobile_secondary', 'Secondary Mobile'),
        ('7_fax_primary', 'Primary Fax'),
        ('8_fax_secondary', 'Secondary Fax'),
        ],
        string='Type', required=True, index=True)
    phone = Phone('Phone', required=False, partner_field='partner_id')
    email = fields.Char(string='E-Mail')
    note = fields.Char('Note')

    @api.onchange('type')
    def type_change(self):
        if self.type:
            if self.type in EMAIL_TYPES:
                self.phone = False
            elif self.type in PHONE_TYPES:
                self.email = False

    @api.constrains('type', 'phone', 'email')
    def _check_partner_phone(self):
        for rec in self:
            if rec.type in EMAIL_TYPES:
                if not rec.email:
                    raise ValidationError(_(
                        "E-mail field must have a value when type is Primary E-mail or Secondary E-mail."))
                if rec.phone:
                    raise ValidationError(_(
                        "Phone field must be empty when type is Primary E-mail or Secondary E-mail."))
            elif rec.type in PHONE_TYPES:
                if not rec.phone:
                    raise ValidationError(_(
                        "Phone field must have a value when type is Primary/Secondary Phone, Primary/Secondary Mobile or Primary/Secondary Fax."))
                if rec.email:
                    raise ValidationError(_(
                        "E-mail field must be empty when type is Primary/Secondary Phone, Primary/Secondary Mobile or Primary/Secondary Fax."))

    def name_get(self):
        res = []
        for pphone in self:
            if pphone.partner_id:
                if self._context.get('callerid'):
                    name = pphone.partner_id.display_name
                else:
                    name = u'%s (%s)' % (pphone.phone, pphone.partner_id.name)
            else:
                name = pphone.phone
            res.append((pphone.id, name))
        return res

    @api.model_cr
    def init(self):
        self._cr.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS single_email_primary
            ON res_partner_phone (partner_id, type)
            WHERE (type='1_email_primary')
            ''')
        self._cr.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS single_phone_primary
            ON res_partner_phone (partner_id, type)
            WHERE (type='3_phone_primary')
            ''')
        self._cr.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS single_mobile_primary
            ON res_partner_phone (partner_id, type)
            WHERE (type='5_mobile_primary')
            ''')
        self._cr.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS single_fax_primary
            ON res_partner_phone (partner_id, type)
            WHERE (type='7_fax_primary')
            ''')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # in v10, we are supposed to have in DB E.164 format
    # with the current implementation, we have:
    # in res.partner : PhoneNumberFormat.INTERNATIONAL
    # in res.partner.phone : E.164
    # It is not good, but it is not a big bug and it's complex to fix
    # so let's let it like that. In v12, we store in
    # PhoneNumberFormat.INTERNATIONAL, so this bug is kind of an anticipation
    # for the future :)

    phone_ids = fields.One2many(
        'res.partner.phone', 'partner_id', string='Phones')
    phone = Phone(
        compute='_compute_partner_phone',
        store=True, readonly=True, compute_sudo=True)
    mobile = Phone(
        compute='_compute_partner_phone',
        store=True, readonly=True, compute_sudo=True)
    fax = Fax(
        compute='_compute_partner_phone',
        store=True, readonly=True, compute_sudo=True)
    email = fields.Char(
        compute='_compute_partner_phone',
        store=True, readonly=True, compute_sudo=True)

    @api.depends('phone_ids.phone', 'phone_ids.type', 'phone_ids.email')
    def _compute_partner_phone(self):
        for partner in self:
            phone = mobile = fax = email = False
            for pphone in partner.phone_ids:
                if pphone.type == '1_email_primary' and pphone.email:
                    email = pphone.email
                elif pphone.phone:
                    if pphone.type == '5_mobile_primary':
                        mobile = pphone.phone
                    elif pphone.type == '7_fax_primary':
                        fax = pphone.phone
                    elif pphone.type == '3_phone_primary':
                        phone = pphone.phone
            partner.phone = phone
            partner.mobile = mobile
            partner.fax = fax
            partner.email = email

    def _update_create_vals(
            self, vals, type, partner_field, partner_phone_field):
        if vals.get(partner_field):
            vals['phone_ids'].append(
                (0, 0, {'type': type, partner_phone_field: vals[partner_field]}))

    @api.model
    def create(self, vals):
        if 'phone_ids' not in vals:
            vals['phone_ids'] = []
            self._update_create_vals(vals, '1_email_primary', 'email', 'email')
            self._update_create_vals(vals, '3_phone_primary', 'phone', 'phone')
            self._update_create_vals(vals, '5_mobile_primary', 'mobile', 'phone')
            self._update_create_vals(vals, '7_fax_primary', 'fax', 'phone')
        return super(ResPartner, self).create(vals)

    def _update_write_vals(
            self, vals, type, partner_field, partner_phone_field):
        self.ensure_one()
        rppo = self.env['res.partner.phone']
        if partner_field in vals:
            pphone = rppo.search([
                ('partner_id', '=', self.id),
                ('type', '=', type)], limit=1)
            if vals[partner_field]:
                if pphone:
                    vals['phone_ids'].append((1, pphone.id, {
                        partner_phone_field: vals[partner_field]}))
                else:
                    vals['phone_ids'].append((0, 0, {
                        'type': type,
                        partner_phone_field: vals[partner_field],
                        }))
            else:
                if pphone:
                    vals['phone_ids'].append((2, pphone.id))

    def write(self, vals):
        if 'phone_ids' not in vals:
            for rec in self:
                vals['phone_ids'] = []
                rec._update_write_vals(vals, '1_email_primary', 'email', 'email')
                rec._update_write_vals(vals, '3_phone_primary', 'phone', 'phone')
                rec._update_write_vals(vals, '5_mobile_primary', 'mobile', 'phone')
                rec._update_write_vals(vals, '7_fax_primary', 'fax', 'phone')
                super(ResPartner, rec).write(vals)
            return True
        else:
            return super(ResPartner, self).write(vals)
