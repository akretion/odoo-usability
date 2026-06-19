# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tracking = fields.Selection(default=False)  # disable default value, so that odoo always goes throught the compute method

    @api.depends('detailed_type')
    def compute_is_storable(self):
        super().compute_is_storable()
        type_mapping = self._detailed_type_mapping_props()
        for record in self:
            if record.detailed_type and record.detailed_type in type_mapping and 'is_storable' in type_mapping[record.detailed_type]:
                record.is_storable = type_mapping[record.detailed_type]['is_storable']

    @api.depends('detailed_type')
    def _compute_tracking(self):
        super()._compute_tracking()
        type_mapping = self._detailed_type_mapping_props()
        for record in self:
            if record.detailed_type and record.detailed_type in type_mapping and 'tracking' in type_mapping[record.detailed_type]:
                record.tracking = type_mapping[record.detailed_type]['tracking']
            else:
                record.tracking = 'none'

    @api.constrains('detailed_type', 'tracking', 'is_storable')
    def _check_detailed_type_stock(self):
        type_mapping_props = self._detailed_type_mapping_props()
        detail_type2label = dict(self.fields_get('detailed_type', 'selection')['detailed_type']['selection'])
        tracking2label = dict(self.fields_get('tracking', 'selection')['tracking']['selection'])
        for record in self:
            if record.detailed_type:
                props = type_mapping_props[record.detailed_type]
                if 'is_storable' in props and props['is_storable'] != record.is_storable:
                    raise ValidationError(self.env._(
                        "Product '%(product)s' is configured with Product Type "
                        "'%(detailed_type)s', so the option Track Inventory must "
                        "be set to %(is_storable)s.",
                        product=record.display_name,
                        detailed_type=detail_type2label[record.detailed_type],
                        is_storable=props['is_storable']))
                if props.get('tracking') and props['tracking'] != record.tracking:
                    raise ValidationError(self.env._(
                        "Product '%(product)s' is configured with Product Type "
                        "'%(detailed_type)s', so tracability must be set "
                        "to '%(tracking)s'.",
                        product=record.display_name,
                        detailed_type=detail_type2label[record.detailed_type],
                        tracking=tracking2label[props['tracking']]))
