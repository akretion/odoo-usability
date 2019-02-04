# Copyright 2017-2019 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_type = fields.Selection(track_visibility='onchange')
    expense_policy = fields.Selection(track_visibility='onchange')
    invoice_policy = fields.Selection(track_visibility='onchange')
    sale_line_warn = fields.Selection(track_visibility='onchange')
