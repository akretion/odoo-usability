# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# @author Alexis de Lattre <alexis.delattre@akretion.com>

from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    probability = fields.Float(track_visibility='onchange')
    date_deadline = fields.Date(track_visibility='onchange')
    # Change from 'always' to 'onchange'
    planned_revenue = fields.Float(track_visibility='onchange')
    type = fields.Selection(track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')
    probable_revenue = fields.Monetary(
        compute='_compute_probable_revenue',
        string='Probable Revenue',
        help="Probable Revenue = Expected Revenue x Probability",
        currency_field='company_currency', readonly=True, store=True)

    @api.multi
    @api.depends('probability', 'planned_revenue')
    def _compute_probable_revenue(self):
        for lead in self:
            rev_prob = lead.probability * lead.planned_revenue / 100.0
            lead.probable_revenue = rev_prob


class CrmLeadTag(models.Model):
    _inherit = 'crm.lead.tag'

    name = fields.Char(translate=False)
