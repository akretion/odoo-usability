# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class LinkTrackerClick(models.Model):
    _inherit = 'link.tracker.click'

    mail_stat_recipient = fields.Char(
        related='mail_stat_id.recipient', store=True)
