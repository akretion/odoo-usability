# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import float_compare


class StockPicking(models.Model):
    _inherit = "stock.picking"

    show_print_zpl_barcode = fields.Boolean(compute='_compute_show_print_zpl_barcode')

    @api.depends('state')
    def _compute_show_print_zpl_barcode(self):
        prec = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for picking in self:
            show = False
            if picking.state == 'done' and picking.picking_type_code != 'outgoing':
                for line in picking.move_line_ids:
                    if (
                            line.product_id.must_print_barcode and
                            float_compare(line.qty_done, 0, precision_digits=prec) > 0):
                        show = True
            picking.show_print_zpl_barcode = show
