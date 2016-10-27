# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class BaseLanguageExport(models.TransientModel):
    _inherit = 'base.language.export'

    # Default format for language files = format used by OpenERP modules
    format = fields.Selection(default='po')


class BaseLanguageInstall(models.TransientModel):
    _inherit = 'base.language.install'

    overwrite = fields.Boolean(default=True)
