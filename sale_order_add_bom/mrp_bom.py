# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class MrpBom(models.Model):
    _inherit = 'mrp.bom'
    _rec_name = 'product_id'

    sale_ok = fields.Boolean(related='product_id.sale_ok', store=True, compute_sudo=True)
