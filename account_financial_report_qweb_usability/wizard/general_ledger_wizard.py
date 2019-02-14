# -*- coding: utf-8 -*-
# Copyright 2019 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GeneralLedgerReportWizard(models.TransientModel):
    _inherit = 'general.ledger.report.wizard'

    foreign_currency = fields.Boolean(default=False)

    def onchange_partner_ids(self):
        # Neutralize native onchange method
        return
