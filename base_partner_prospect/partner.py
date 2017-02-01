# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    prospect = fields.Boolean(
        string='Is a Prospect', track_visibility='onchange')

    @api.onchange('customer')
    def prospect_customer_change(self):
        if self.customer and self.prospect:
            self.prospect = False

    @api.onchange('prospect')
    def prospect_change(self):
        if self.prospect and self.customer:
            self.customer = False

    @api.constrains('customer', 'prospect')
    def partner_prospect_check(self):
        for partner in self:
            if partner.customer and partner.prospect:
                raise ValidationError(_(
                    "Partner '%s' cannot be both a prospect and a customer")
                    % self.name_get()[0][1])
