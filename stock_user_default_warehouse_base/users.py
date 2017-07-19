# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    context_default_warehouse_id = fields.Many2one(
        'stock.warehouse', string='Default Warehouse', company_dependent=True,
        help=u"Default warehouse for sale orders (if the module "
        "stock_user_default_warehouse_sale is installed) and purchase orders "
        "(if the module stock_user_default_warehouse_purchase is installed).")
