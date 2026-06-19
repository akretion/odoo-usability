# Copyright 2023 Akretion France (http://www.akretion.com/)
# Copyright 2023 Odoo SA (contains code copy-pasted from Odoo v16)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection([
        ('consu', 'Goods'),
        ('service', 'Service'),
        ('combo', "Combo"),
        ], string='Product Type', default='consu', required=True, tracking=True)
    type = fields.Selection(
        compute='_compute_type', store=True, precompute=True, string="Type",  # native string = "Product Type"
        default=False, required=False)
    uom_id = fields.Many2one(
        compute="_compute_uom_id", store=True, precompute=True, readonly=False)

    def _detailed_type_mapping_props(self):
        # key = detailed_type
        # value = {'type': 'consu', 'uom_id': 2, 'uom_po_id': 3}  # key 'type' is required
        return {
            'consu': {'type': 'consu'},
            'service': {'type': 'service'},
            'combo': {'type': 'combo'},
            }

    @api.depends('detailed_type')
    def _compute_type(self):
        type_mapping_props = self._detailed_type_mapping_props()
        for record in self:
            record.type = type_mapping_props.get(record.detailed_type, {'type': record.detailed_type})['type']

    @api.depends('detailed_type')
    def _compute_uom_id(self):
        type_mapping_props = self._detailed_type_mapping_props()
        for record in self:
            if record.detailed_type and record.detailed_type in type_mapping_props and type_mapping_props[record.detailed_type].get('uom_id'):
                record.uom_id = type_mapping_props[record.detailed_type]['uom_id']

    @api.depends('detailed_type')
    def _compute_uom_po_id(self):
        super()._compute_uom_po_id()
        type_mapping_props = self._detailed_type_mapping_props()
        for record in self:
            if record.detailed_type and record.detailed_type in type_mapping_props:
                if type_mapping_props[record.detailed_type].get('uom_po_id'):
                    record.uom_po_id = type_mapping_props[record.detailed_type]['uom_po_id']

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

    @api.constrains('detailed_type', 'type', 'uom_id', 'uom_po_id')
    def _check_detailed_type(self):
        type_mapping_props = self._detailed_type_mapping_props()
        detail_type2label = dict(self.fields_get('detailed_type', 'selection')['detailed_type']['selection'])
        type2label = dict(self.fields_get('type', 'selection')['type']['selection'])
        for record in self:
            if record.detailed_type:
                props = type_mapping_props[record.detailed_type]
                if props['type'] != record.type:
                    raise ValidationError(self.env._(
                        "Product '%(product)s' is configured with Product Type "
                        "'%(detailed_type)s', so it's Type must be '%(type)s'.",
                        product=record.display_name,
                        detailed_type=detail_type2label[record.detailed_type],
                        type=type2label[record.type]))
                if props.get('uom_id') and record.uom_id.id != props['uom_id']:
                    uom_name = self.env['uom.uom'].browse(props['uom_id']).display_name
                    raise ValidationError(self.env._(
                        "Product '%(product)s' is configured with Product Type "
                        "'%(detailed_type)s', so it's unit of measure "
                        "must be '%(uom)s'.",
                        product=record.display_name,
                        detailed_type=detail_type2label[record.detailed_type],
                        uom=uom_name))
                if props.get('uom_po_id') and record.uom_po_id.id != props['uom_po_id']:
                    uom_po_name = self.env['uom.uom'].browse(props['uom_po_id']).display_name
                    raise ValidationError(self.env._(
                        "Product '%(product)s' is configured with Product Type "
                        "'%(detailed_type)s', so it's purchase unit of measure "
                        "must be '%(uom)s'.",
                        product=record.display_name,
                        detailed_type=detail_type2label[record.detailed_type],
                        uom=uom_po_name))
