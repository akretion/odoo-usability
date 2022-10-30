# Copyright 2021-2022 Akretion France (https://akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    # Similar to the field static_invoice_terms in account_usability
    static_sale_terms = fields.Text(
        translate=True, string="Legal Terms on Quotation")
