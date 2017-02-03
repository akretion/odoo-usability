# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    track_all = fields.Boolean(track_visibility='onchange')
    track_incoming = fields.Boolean(track_visibility='onchange')
    track_outgoing = fields.Boolean(track_visibility='onchange')
    sale_delay = fields.Float(track_visibility='onchange')
