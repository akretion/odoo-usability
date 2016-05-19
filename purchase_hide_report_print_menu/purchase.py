# -*- coding: utf-8 -*-
# © 2016 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        context = self._context
        res = super(PurchaseOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if ('purchase_order' in context and 'toolbar' in res and
                'print' in res['toolbar']):
            report_purchase_quotation = self.env.ref(
                'purchase.report_purchase_quotation')
            list_print_submenu_to_hide = []
            for print_submenu in res['toolbar']['print']:
                if print_submenu['id'] in [report_purchase_quotation.id]:
                    list_print_submenu_to_hide.append(print_submenu)
            for print_submenu_to_hide in list_print_submenu_to_hide:
                res['toolbar']['print'].remove(print_submenu_to_hide)
        return res
