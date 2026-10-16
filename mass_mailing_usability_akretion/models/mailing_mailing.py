# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MassMailing(models.Model):
    _inherit = 'mailing.mailing'

    # keep_archives parameter sets 'auto_delete' on mail object
    # and I want to store outgoing mails by default in odoo, to have
    # a better diagnostic in case of technical problem
    keep_archives = fields.Boolean(default=True)
