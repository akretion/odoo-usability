# -*- coding: utf-8 -*-
# Copyright (C) 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('credit', 'debit')
    def _compute_balance(self):
        for partner in self:
            partner.balance = partner.credit - partner.debit

    # The field 'currency_id' defined in the account module
    # is a computed field that gets the company currency
    balance = fields.Monetary(
        compute='_compute_balance', readonly=True,
        string="Account Balance")

    def open_aged_open_invoices_report(self):
        wiz = self.env['aged.partner.balance.wizard'].create({
            'show_move_line_details': True,
            'partner_ids': [(6, 0, self.ids)],
        })
        action = wiz.button_export_pdf()
        return action
