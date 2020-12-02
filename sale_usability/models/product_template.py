# Copyright 2017-2019 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_type = fields.Selection(tracking=True)
    expense_policy = fields.Selection(tracking=True)
    invoice_policy = fields.Selection(tracking=True)
    sale_line_warn = fields.Selection(tracking=True)
