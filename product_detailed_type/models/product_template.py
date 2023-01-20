# Copyright 2023 Akretion France (http://www.akretion.com/)
# Copyright 2023 Odoo SA (contains code copy-pasted from Odoo v16)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ], string='Product Type', default='consu', required=True, tracking=True)
    type = fields.Selection(compute='_compute_type', store=True, string="Type")

    def _detailed_type_mapping(self):
        return {}

    @api.depends('detailed_type')
    def _compute_type(self):
        type_mapping = self._detailed_type_mapping()
        for record in self:
            record.type = type_mapping.get(record.detailed_type, record.detailed_type)
