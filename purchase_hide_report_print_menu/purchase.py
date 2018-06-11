# -*- coding: utf-8 -*-
# © 2016 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        res = super(PurchaseOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if self._context.get('purchase_order', False):
            report_purchase_quotation = self.env.ref(
                'purchase.report_purchase_quotation')
            for print_submenu in res.get('toolbar', {}).get('print', []):
                if print_submenu['id'] == report_purchase_quotation.id:
                    res['toolbar']['print'].remove(print_submenu)
        return res
