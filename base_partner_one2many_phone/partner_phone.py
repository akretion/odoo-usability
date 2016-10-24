# -*- coding: utf-8 -*-
# © 2014-2016 Abbaye du Barroux (http://www.barroux.org)
# © 2016 Akretion (http://www.akretion.com>)
# @author: Frère Bernard <informatique@barroux.org>
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
from odoo.addons.base_phone.fields import Phone, Fax


class ResPartnerPhone(models.Model):
    _name = 'res.partner.phone'
    _order = 'partner_id, type'

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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('phone_ids.phone', 'phone_ids.type')
    def _compute_partner_phone(self):
        phone = mobile = fax = False
        for partner_phone in self.phone_ids:
            not_phone_type = ('2_mobile', '4_home_fax', '5_office_fax')
            if partner_phone.type not in not_phone_type:
                phone = partner_phone.phone
            if partner_phone.type == '2_mobile':
                mobile = partner_phone.phone
            if partner_phone.type in ('5_office_fax', '4_home_fax'):
                fax = partner_phone.phone
        self.phone = phone
        self.mobile = mobile
        self.fax = fax

    phone_ids = fields.One2many(
        'res.partner.phone', 'partner_id', string='Phones')
    phone = Phone(
        compute='_compute_partner_phone', store=True, readonly=True)
    mobile = Phone(
        compute='_compute_partner_phone', store=True, readonly=True)
    fax = Fax(
        compute='_compute_partner_phone', store=True, readonly=True)
