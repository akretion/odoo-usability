# -*- coding: utf-8 -*-
# © 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, tools, api


class PosSaleReport(models.Model):
    _name = 'pos.sale.report'
    _description = 'POS orders and Sale orders aggregated report'
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Date(string='Order Date', readonly=True)
    product_id = fields.Many2one(
        'product.product', string='Product Variant', readonly=True)
    product_categ_id = fields.Many2one(
        'product.category', string='Product Category', readonly=True)
    pos_categ_id = fields.Many2one(
        'pos.category', string='Point of Sale Category', readonly=True)
    product_tmpl_id = fields.Many2one(
        'product.template', string='Product', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', readonly=True)
    origin = fields.Char(string='Origin', readonly=True)
    qty = fields.Float(string='Quantity', readonly=True)

    # WARNING : this code doesn't handle uom conversion for the moment
    def _sale_order_select(self):
        select = """SELECT min(sol.id)*-1 AS id,
            so.date_order::date AS date,
            sol.product_id AS product_id,
            pt.categ_id AS product_categ_id,
            pt.pos_categ_id AS pos_categ_id,
            pp.product_tmpl_id AS product_tmpl_id,
            so.company_id AS company_id,
            'Sale Order' AS origin,
            sum(sol.product_uom_qty) AS qty
            FROM sale_order_line sol
            LEFT JOIN sale_order so ON so.id = sol.order_id
            LEFT JOIN product_product pp ON pp.id = sol.product_id
            LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
            WHERE so.state NOT IN ('draft', 'sent', 'cancel')
            GROUP BY so.date_order, sol.product_id, pp.product_tmpl_id,
            so.company_id, pt.categ_id, pt.pos_categ_id
        """
        return select

    def _pos_order_select(self):
        select = """SELECT min(pol.id) AS id,
            po.date_order::date AS date,
            pol.product_id AS product_id,
            pt.categ_id AS product_categ_id,
            pt.pos_categ_id AS pos_categ_id,
            pp.product_tmpl_id AS product_tmpl_id,
            po.company_id AS company_id,
            'Point of Sale' AS origin,
            sum(pol.qty) AS qty
            FROM pos_order_line pol
            LEFT JOIN pos_order po ON po.id = pol.order_id
            LEFT JOIN product_product pp ON pp.id = pol.product_id
            LEFT JOIN product_template pt ON pt.id = pp.product_tmpl_id
            WHERE po.state IN ('paid', 'done', 'invoiced')
            GROUP BY po.date_order, pol.product_id, pp.product_tmpl_id,
            po.company_id, pt.categ_id, pt.pos_categ_id
        """
        return select

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("CREATE OR REPLACE VIEW %s AS (%s UNION %s)" % (
            self._table, self._sale_order_select(), self._pos_order_select()))
