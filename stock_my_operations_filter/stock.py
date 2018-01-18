# -*- coding: utf-8 -*-
# © 2015-2018 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    default_picking_type_ids = fields.Many2many(
        'stock.picking.type', 'stock_picking_type_users_rel',
        'user_id', 'picking_type_id', string='Default Stock Operations')


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    default_user_ids = fields.Many2many(
        'res.users', 'stock_picking_type_users_rel',
        'picking_type_id', 'user_id', string='Visible by Default by')
