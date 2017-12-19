# -*- coding: utf-8 -*-
# © 2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class LunchVoucherPurchase(models.TransientModel):
    _inherit = 'lunch.voucher.purchase'

    def run(self):
        self.ensure_one()
        action = super(LunchVoucherPurchase, self).run()
        company = self.env.user.company_id
        # force_company to read standard_price properly
        company = company.with_context(force_company=company.id)
        lvao = self.env['lunch.voucher.attribution']
        assert self._context.get('active_model')\
            == 'lunch.voucher.attribution', 'wrong source model'
        assert self._context.get('active_ids'), 'missing active_ids in ctx'
        if not company.lunch_voucher_natixis_customer_code:
            raise UserError(_(
                "Missing Natixis Customer Ref on company '%s'.")
                % company.name)
        if not company.lunch_voucher_natixis_delivery_code:
            raise UserError(_(
                "Missing Natixis Delivery Code on company '%s'.")
                % company.name)
        if len(company.lunch_voucher_natixis_customer_code) != 7:
            raise UserError(_(
                "Natixis Customer Ref '%s' on company '%s' should "
                "have 7 characters/digits.")
                % (company.lunch_voucher_natixis_customer_code, company.name))
        if len(company.lunch_voucher_natixis_delivery_code) != 7:
            raise UserError(_(
                "Natixis Delivery Code on company '%s' should "
                "have 7 characters/digits.")
                % (company.lunch_voucher_natixis_delivery_code, company.name))
        if float_is_zero(
                company.lunch_voucher_employer_price,
                precision_digits=2):
            raise UserError(_(
                "Lunch Voucher Employer Price not set on company '%s'.")
                % company.name)
        if float_is_zero(
                company.lunch_voucher_product_id.seller_ids[0].price,
                precision_digits=2):
            raise UserError(_(
                "Lunch Voucher Price on supplier info is not set "
                "on product '%s'.")
                % company.lunch_voucher_product_id.display_name)
        lvouchers = lvao.browse(self._context['active_ids'])
        of = u''
        tmp = {}
        price = company.lunch_voucher_product_id.seller_ids[0].price
        for lvoucher in lvouchers:
            if lvoucher.qty > 0:
                if lvoucher.qty not in tmp:
                    tmp[lvoucher.qty] = 1
                else:
                    tmp[lvoucher.qty] += 1
        for vouchers_per_pack, pack_qty in tmp.iteritems():
            if vouchers_per_pack > 99:
                raise UserError(_(
                    "Cannot order more than 99 vouchers per pack"))
            line = u'%s%s%s%s%s%s%s%s\n' % (
                company.lunch_voucher_natixis_delivery_code,
                company.lunch_voucher_natixis_customer_code,
                unicode(pack_qty).zfill(3),
                unicode(vouchers_per_pack).zfill(2),
                unicode(pack_qty * vouchers_per_pack).zfill(5),
                '{:05.2f}'.format(price),
                '{:05.2f}'.format(company.lunch_voucher_employer_price),
                ' ' * 64)
            of += line
        today_dt = fields.Date.from_string(
            fields.Date.context_today(self))
        filename = 'E%s_%s.txt' % (
            company.lunch_voucher_natixis_customer_code,
            today_dt.strftime('%d%m%Y'))
        self.env['ir.attachment'].create({
            'name': filename,
            'res_id': action['res_id'],
            'res_model': 'purchase.order',
            'datas': of.encode('base64'),
            'datas_fname': filename,
            'type': 'binary',
            })
        return action
