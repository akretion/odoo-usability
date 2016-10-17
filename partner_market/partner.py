# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartnerMarket(models.Model):
    _name = 'res.partner.market'
    _description = 'Market'

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [(
        'name_uniq',
        'unique(name)',
        'This market already exists!'
        )]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    market_id = fields.Many2one(
        'res.partner.market', string='Market', ondelete='restrict', copy=False)
    # Field only displayed on customers with parent_id = False

    @api.model
    def _commercial_fields(self):
        res = super(ResPartner, self)._commercial_fields()
        res.append('market_id')
        return res
