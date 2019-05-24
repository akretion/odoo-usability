# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models


class MailMailStatistics(models.Model):
    _inherit = 'mail.mail.statistics'

    recipient = fields.Char(store=True)

    # add invalidation for 'recipient' field
    @api.depends('res_id', 'model')
    def _compute_recipient(self):
        return super(MailMailStatistics, self)._compute_recipient()
