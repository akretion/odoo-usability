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
    type = fields.Selection(
        compute='_compute_type', store=True, string="Type",  # native string = "Product Type"
        default=False, required=False)

    def _detailed_type_mapping(self):
        return {}

    @api.depends('detailed_type')
    def _compute_type(self):
        type_mapping = self._detailed_type_mapping()
        for record in self:
            record.type = type_mapping.get(record.detailed_type, record.detailed_type)

    # to ensure compat with test and demo data
    # It's not perfect, we still have a problem when installing the "stock"
    # module while product_detailed_type_stock is not installed yet: it creates
    # products with type = 'product' and with the inherit below, it sets detailed_type = 'product'
    # but this value is only possible once product_detailed_type_stock is installed. Odoo says:
    # ValueError: Wrong value for product.template.detailed_type: 'product'
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('type') and vals['type'] != vals.get('detailed_type'):
                vals['detailed_type'] = vals['type']
        return super().create(vals_list)
