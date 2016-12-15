# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # track_visibility is handled in the 'mail' module, and base_usability
    # doesn't depend on 'mail', but that doesn't hurt, it will just be
    # ignored if mail is not installed
    name = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    ref = fields.Char(track_visibility='onchange')
    lang = fields.Selection(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    vat = fields.Char(track_visibility='onchange')
    customer = fields.Boolean(track_visibility='onchange')
    supplier = fields.Boolean(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    street = fields.Char(track_visibility='onchange')
    street2 = fields.Char(track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    city = fields.Char(track_visibility='onchange')
    state_id = fields.Many2one(track_visibility='onchange')
    country_id = fields.Many2one(track_visibility='onchange')
    email = fields.Char(track_visibility='onchange')
    is_company = fields.Boolean(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    # For reports
    name_title = fields.Char(
        compute='_compute_name_title', string='Name with Title')

    @api.multi
    @api.depends('name', 'title')
    def _compute_name_title(self):
        for partner in self:
            name_title = partner.name
            if partner.title and not partner.is_company:
                partner_lg = partner
                # If prefer to read the lang of the partner than the lang
                # of the context. That way, an English man will be displayed
                # with his title in English whatever the environment
                if partner.lang:
                    partner_lg = partner.with_context(lang=partner.lang)
                title = partner_lg.title.shortcut or partner_lg.title.name
                name_title = u' '.join([title, name_title])
            partner.name_title = name_title

    @api.multi
    def _display_address(self, without_company=False):
        '''Remove empty lines'''
        res = super(ResPartner, self)._display_address(
            without_company=without_company)
        while "\n\n" in res:
            res = res.replace('\n\n', '\n')
        return res
