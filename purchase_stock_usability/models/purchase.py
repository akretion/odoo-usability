# Copyright 2015-2021 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_type_id = fields.Many2one(tracking=True)
    incoterm_id = fields.Many2one(tracking=True)

    # inherit compute method of the field delivery_partner_id
    # defined in purchase_usability
    @api.depends('dest_address_id', 'picking_type_id')
    def _compute_delivery_partner_id(self):
        for o in self:
            delivery_partner_id = False
            if o.dest_address_id:
                delivery_partner_id = o.dest_address_id
            elif (
                    o.picking_type_id.warehouse_id and
                    o.picking_type_id.warehouse_id.partner_id):
                delivery_partner_id = o.picking_type_id.warehouse_id.partner_id
            o.delivery_partner_id = delivery_partner_id
