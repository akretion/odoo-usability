# -*- coding: utf-8 -*-
# © 2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.report import report_sxw


class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'group_lines': self._group_lines,
            })

    def _group_lines(self, inventory, context=None):
        assert inventory, 'Missing inventory'
        self.cr.execute("""
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
            """, (inventory.id, ))
        res = []
        silo = self.pool['stock.inventory.line']
        for row in self.cr.dictfetchall():
            row['min_line'] = silo.browse(
                self.cr, self.uid, row['min_line_id'], context=context)
            res.append(row)
        return res
