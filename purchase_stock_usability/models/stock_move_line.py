# Copyright 2023 Akretion France (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    # for optional display in tree view
    product_supplier_code = fields.Char(
        compute='_compute_product_supplier_code', string="Vendor Product Code")

    def _compute_product_supplier_code(self):
        pso = self.env['product.supplierinfo']
        for mline in self:
            code = False
            move = mline.move_id
            if move and move.purchase_line_id and move.purchase_line_id.order_id:
                po = move.purchase_line_id.order_id
                partner_id = po.partner_id.commercial_partner_id.id
                if partner_id:
                    sinfo = pso.search_read([
                        ('product_code', '!=', False),
                        ('partner_id', '=', partner_id),
                        ('company_id', 'in', (False, mline.company_id.id)),
                        ('product_id', 'in', (False, mline.product_id.id)),
                        ], ['product_code'], limit=1, order='product_id')
                    # if I order by product_id, I get the null values at the end
                    if sinfo:
                        code = sinfo[0]['product_code']
            mline.product_supplier_code = code
