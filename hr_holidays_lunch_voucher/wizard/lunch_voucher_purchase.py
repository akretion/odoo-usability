# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, _
from odoo.exceptions import UserError


class LunchVoucherPurchase(models.TransientModel):
    _name = 'lunch.voucher.purchase'
    _description = 'Purchase Lunch Vouchers Wizard'

    def run(self):
        self.ensure_one()
        company = self.env.user.company_id
        if not company.lunch_voucher_product_id:
            raise UserError(_(
                "Lunch Voucher Product not configured on company %s")
                % company.name)
        if not company.lunch_voucher_product_id.seller_ids:
            raise UserError(_(
                "Missing supplier on Product '%s'.")
                % company.lunch_voucher_product_id.name)

        poo = self.env['purchase.order']
        polo = self.env['purchase.order.line']
        lvao = self.env['lunch.voucher.attribution']
        assert self._context.get('active_model') ==\
            'lunch.voucher.attribution', 'wrong source model'
        assert self._context.get('active_ids'), 'missing active_ids in ctx'
        lvouchers = lvao.browse(self._context['active_ids'])
        total_qty = 0
        for lvoucher in lvouchers:
            if lvoucher.purchase_id:
                raise UserError(_(
                    "One of the Lunch Voucher Attributions you selected "
                    "related to employee '%s' is already linked to a "
                    "purchase order.") % lvoucher.employee_id.name)
            if lvoucher.qty < 0:
                raise UserError(_(
                    "One of the Lunch Voucher Attributions you selected "
                    "related to employee '%s' has a negative quantity.")
                    % lvoucher.employee_id.name)
            total_qty += lvoucher.qty

        supplier = company.lunch_voucher_product_id.seller_ids[0].name
        pick_type_id = poo.default_get(['picking_type_id'])['picking_type_id']
        vals = {'picking_type_id': pick_type_id, 'partner_id': supplier.id}
        vals = poo.play_onchanges(vals, ['picking_type_id'])
        vals = poo.play_onchanges(vals, ['partner_id'])

        lvals = {
            'product_id': company.lunch_voucher_product_id.id,
            'order_id': vals, 'product_qty': total_qty}
        lvals = polo.play_onchanges(lvals, ['product_id'])
        # TODO check lvals['taxes_id'] uses (6, 0, ...)
        lvals.pop('order_id')
        vals['order_line'] = [(0, 0, lvals)]
        po = poo.create(vals)
        lvouchers.write({'purchase_id': po.id})

        action = self.env['ir.actions.act_window'].for_xml_id(
            'purchase', 'purchase_rfq')
        action.update({
            'res_id': po.id,
            'view_mode': 'form,tree',
            'views': False,
            })
        return action
