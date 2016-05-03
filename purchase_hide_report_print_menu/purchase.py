# -*- coding: utf-8 -*-
# © 2016 Chafique DELLI @ Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}
        res = super(PurchaseOrder, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=submenu)
        if ('purchase_order' in context and 'toolbar' in res and
                'print' in res['toolbar']):
            model_data_obj = self.pool['ir.model.data']
            report_purchase_quotation_id = model_data_obj.xmlid_to_res_id(
                cr, uid, 'purchase.report_purchase_quotation',
                raise_if_not_found=True)
            list_print_submenu_to_hide = []
            for print_submenu in res['toolbar']['print']:
                if print_submenu['id'] in [report_purchase_quotation_id]:
                    list_print_submenu_to_hide.append(print_submenu)
            for print_submenu_to_hide in list_print_submenu_to_hide:
                res['toolbar']['print'].remove(print_submenu_to_hide)
        return res
