# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id = fields.Many2one(track_visibility='onchange')
    incoterm = fields.Many2one(track_visibility='onchange')
