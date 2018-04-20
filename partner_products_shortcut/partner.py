# -*- coding: utf-8 -*-
# © 2014-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _product_supplied_count(self):
        for partner in self:
            count = False
            try:
                sellers = self.env['product.supplierinfo'].search(
                    [('name', '=', partner.id)])
                if sellers:
                    pproducts = self.env['product.product'].search(
                        [('seller_ids', 'in', sellers.ids)])
                    count = len(pproducts)
            except:
                pass
            partner.product_supplied_count = count

    product_supplied_count = fields.Integer(
        compute='_product_supplied_count', string="# of Products Supplied",
        readonly=True)

    @api.multi
    def show_supplied_products(self):
        self.ensure_one()
        sellers = self.env['product.supplierinfo'].search(
            [('name', '=', self.id)])
        if not sellers:
            raise UserError(_(
                "The supplier '%s' is not linked to any product") % self.name)
        pproducts = self.env['product.product'].search(
            [('seller_ids', 'in', sellers.ids)])
        action = self.env['ir.actions.act_window'].for_xml_id(
            'product', 'product_normal_action')
        action.update({
            'domain': "[('id', 'in', %s)]" % pproducts.ids,
            })
        return action
