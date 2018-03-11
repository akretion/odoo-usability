# -*- coding: utf-8 -*-
# Copyright 2016-2018 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def report_group_lines(self):
        self.ensure_one()
        self._cr.execute("""
            SELECT
            min(id) AS min_line_id,
            product_id,
            package_id,
            prod_lot_id,
            product_uom_id,
            standard_price,
            sum(product_qty) AS product_qty,
            sum(theoretical_qty) AS theoretical_qty
            FROM stock_inventory_line
            WHERE inventory_id=%s
            GROUP BY product_id, package_id, prod_lot_id,
                     product_uom_id, standard_price
            """, (self.id, ))
        res = []
        silo = self.env['stock.inventory.line']
        for row in self._cr.dictfetchall():
            row['min_line'] = silo.browse(row['min_line_id'])
            res.append(row)
        return res
