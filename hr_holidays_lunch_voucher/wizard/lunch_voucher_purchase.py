# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, _
from openerp.exceptions import Warning as UserError


class LunchVoucherPurchase(models.TransientModel):
    _name = 'lunch.voucher.purchase'
    _description = 'Purchase Lunch Vouchers Wizard'

    @api.multi
    def run(self):
        self.ensure_one()
        company = self.env.user.company_id
        if not company.lunch_voucher_product_id:
            raise UserError(_(
                "Lunch Voucher Product not configured on company %s")
                % company.name)
        if not company.lunch_voucher_product_id.seller_id:
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

        supplier = company.lunch_voucher_product_id.seller_id
        pick_type_id = poo.default_get(['picking_type_id'])['picking_type_id']
        onchange_ptype_vals = poo.browse(False).onchange_picking_type_id(
            pick_type_id)
        vals = onchange_ptype_vals['value']
        onchange_vals = poo.browse(False).onchange_partner_id(supplier.id)
        vals.update(onchange_vals['value'])
        vals['partner_id'] = supplier.id

        product = company.lunch_voucher_product_id
        onchange_product_vals = polo.browse(False).onchange_product_id(
            vals.get('pricelist_id'), product.id, total_qty, False,
            supplier.id, fiscal_position_id=vals.get('fiscal_position_id'))
        lvals = onchange_product_vals['value']
        lvals['product_id'] = product.id
        lvals['product_qty'] = total_qty
        if lvals['taxes_id']:
            lvals['taxes_id'] = [(6, 0, lvals['taxes_id'])]
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
