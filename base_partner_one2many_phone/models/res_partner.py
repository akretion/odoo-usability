# Copyright 2014-2023 Abbaye du Barroux (http://www.barroux.org)
# Copyright 2016-2023 Akretion (http://www.akretion.com>)
# @author: Frère Bernard <informatique@barroux.org>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, Command


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
        'res.partner.phone', 'partner_id', string='Phones/Emails')
    phone = fields.Char(compute='_compute_partner_phone', store=True)
    mobile = fields.Char(compute='_compute_partner_phone', store=True)
    email = fields.Char(compute='_compute_partner_phone', store=True)

    @api.depends('phone_ids.phone', 'phone_ids.type', 'phone_ids.email')
    def _compute_partner_phone(self):
        for partner in self:
            phone = mobile = email = False
            for pphone in partner.phone_ids:
                if pphone.type == '1_email_primary' and pphone.email:
                    email = pphone.email
                elif pphone.phone:
                    if pphone.type == '5_mobile_primary':
                        mobile = pphone.phone
                    elif pphone.type == '3_phone_primary':
                        phone = pphone.phone
            partner.phone = phone
            partner.mobile = mobile
            partner.email = email

    def _update_create_vals(
            self, vals, type, partner_field, partner_phone_field):
        if vals.get(partner_field):
            vals['phone_ids'].append(
                Command.create({'type': type, partner_phone_field: vals[partner_field]}))
        if partner_field in vals:
            vals.pop(partner_field)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'phone_ids' not in vals:
                vals['phone_ids'] = []
                self._update_create_vals(vals, '1_email_primary', 'email', 'email')
                self._update_create_vals(vals, '3_phone_primary', 'phone', 'phone')
                self._update_create_vals(vals, '5_mobile_primary', 'mobile', 'phone')
        return super().create(vals_list)

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
                    vals['phone_ids'].append(Command.update(pphone.id, {
                        partner_phone_field: vals[partner_field]}))
                else:
                    vals['phone_ids'].append(Command.create({
                        'type': type,
                        partner_phone_field: vals[partner_field],
                        }))
            else:
                if pphone:
                    vals['phone_ids'].append(Command.delete(pphone.id))
            vals.pop(partner_field)

    def write(self, vals):
        if 'phone_ids' not in vals:
            for rec in self:
                cvals = dict(vals, phone_ids=[])
                rec._update_write_vals(cvals, '1_email_primary', 'email', 'email')
                rec._update_write_vals(cvals, '3_phone_primary', 'phone', 'phone')
                rec._update_write_vals(cvals, '5_mobile_primary', 'mobile', 'phone')
                super(ResPartner, rec).write(cvals)
            return True
        else:
            return super().write(vals)
