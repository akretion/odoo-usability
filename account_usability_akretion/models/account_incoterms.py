# Copyright 2015-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    _code_unique = models.UniqueIndex(
        '(code)',
        'This incoterm code already exists.')
