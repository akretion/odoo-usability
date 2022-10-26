# Copyright 2015-2022 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    # In the 'base' module, they didn't put any string, so the bank name is
    # displayed as 'Name', which the string of the related field it
    # points to
    bank_name = fields.Char(string='Bank Name')
