# Copyright 2016-2019 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    purchase_method = fields.Selection(track_visibility='onchange')
    purchase_line_warn = fields.Selection(track_visibility='onchange')
