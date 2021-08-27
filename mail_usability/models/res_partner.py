# Copyright 2015-2021 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # tracking=True is handled in the 'mail' module, so it's better
    # to have this in mail_usability than in base_usability
    name = fields.Char(tracking=True)
    parent_id = fields.Many2one(tracking=True)
    ref = fields.Char(tracking=True)
    lang = fields.Selection(tracking=True)
    vat = fields.Char(tracking=True)
    street = fields.Char(tracking=True)
    street2 = fields.Char(tracking=True)
    zip = fields.Char(tracking=True)
    city = fields.Char(tracking=True)
    state_id = fields.Many2one(tracking=True)
    country_id = fields.Many2one(tracking=True)
    is_company = fields.Boolean(tracking=True)
    active = fields.Boolean(tracking=True)
    company_id = fields.Many2one(tracking=True)
