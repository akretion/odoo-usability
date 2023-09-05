# Copyright 2014-2023 Abbaye du Barroux (http://www.barroux.org)
# Copyright 2016-2023 Akretion (http://www.akretion.com>)
# @author: Frère Bernard <informatique@barroux.org>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.addons.phone_validation.tools import phone_validation

EMAIL_TYPES = ('1_email_primary', '2_email_secondary')
PHONE_TYPES = ('3_phone_primary', '4_phone_secondary', '5_mobile_primary', '6_mobile_secondary', '7_fax_primary', '8_fax_secondary')


class ResPartnerPhone(models.Model):
    _name = 'res.partner.phone'
    _order = 'partner_id, type'
    _phone_name_sequence = 8
    _description = 'Multiple emails and phones for partners'

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
    phone = fields.Char(string='Phone')
    email = fields.Char(string='E-Mail')
    note = fields.Char('Note')

    @api.onchange('type')
    def type_change(self):
        if self.type:
            if self.type in EMAIL_TYPES:
                self.phone = False
            elif self.type in PHONE_TYPES:
                self.email = False

    @api.onchange('phone', 'partner_id')
    def _onchange_phone_validation(self):
        if self.phone:
            country = self.partner_id.country_id
            self.phone = phone_validation.phone_format(
                self.phone,
                country.code or None,
                country.phone_code or None,
                force_format='INTERNATIONAL',
                raise_exception=False)

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
