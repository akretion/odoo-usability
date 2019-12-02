# -*- coding: utf-8 -*-
# Copyright 2016-2019 Akretion France
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class MrpBom(models.Model):
    _inherit = 'mrp.bom'
#    _rec_name = 'product_id'

    sale_ok = fields.Boolean(related='product_tmpl_id.sale_ok', store=True)
