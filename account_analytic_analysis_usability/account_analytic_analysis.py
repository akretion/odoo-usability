# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    recurring_next_date = fields.Date(track_visibility='onchange')
    recurring_rule_type = fields.Selection(track_visibility='onchange')
    recurring_interval = fields.Integer(track_visibility='onchange')
    recurring_invoices = fields.Boolean(track_visibility='onchange')
