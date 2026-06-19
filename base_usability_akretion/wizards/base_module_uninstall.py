# Copyright 2026 Akretion France (https://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BaseModuleUninstall(models.TransientModel):
    _inherit = "base.module.uninstall"

    show_all = fields.Boolean(default=True)
