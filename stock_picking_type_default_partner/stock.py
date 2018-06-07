# -*- coding: utf-8 -*-
# Copyright 2014-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    default_partner_id = fields.Many2one(
        'res.partner', string='Default Partner', ondelete='restrict',
        help="If set, it will be the default partner on this type of "
        "pickings.")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _default_partner_id(self):
        if self._context.get('default_picking_type_id'):
            picktype = self.env['stock.picking.type'].browse(
                self._context.get('default_picking_type_id'))
            if picktype.default_partner_id:
                return picktype.default_partner_id
        return False

    partner_id = fields.Many2one(default=_default_partner_id)
