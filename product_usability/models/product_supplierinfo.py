# Copyright 2015-2022 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# @author Raphaël Valyi <rvalyi@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    partner_id = fields.Many2one(domain=[('parent_id', '=', False)])
