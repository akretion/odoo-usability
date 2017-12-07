# -*- coding: utf-8 -*-
# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_warn = fields.Selection(track_visibility='onchange')

    # Fix an access right issue when accessing partner form without being
    # a member of the purchase/User group
    @api.multi
    def _purchase_invoice_count(self):
        poo = self.env['purchase.order']
        aio = self.env['account.invoice']
        for partner in self:
            try:
                partner.purchase_order_count = poo.search_count(
                    [('partner_id', 'child_of', partner.id)])
            except Exception:
                pass
            try:
                partner.supplier_invoice_count = aio.search_count([
                    ('partner_id', 'child_of', partner.id),
                    ('type', '=', 'in_invoice')])
            except Exception:
                pass
