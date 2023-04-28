# Copyright 2023 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    autofill_done = fields.Boolean(readonly=True)

    def button_stock_move_line_autofill(self):
        self.ensure_one()
        prec = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        for ml in self.move_line_ids_without_package:
            if ml.product_id and float_compare(ml.product_uom_qty, 0, precision_digits=prec) > 0 and float_is_zero(ml.qty_done, precision_digits=prec):
                if (
                        ml.product_id.tracking in ('lot', 'serial') and
                        not ml.lot_id and
                        not ml.lot_name):
                    raise UserError(_(
                        "Autofill is not possible: the lot is not set "
                        "on move line with product '%s' quantity %s %s.")
                        % (
                            ml.product_id.display_name,
                            ml.product_uom_qty,
                            ml.product_uom_id.display_name
                        ))
                ml.write({'qty_done': ml.product_uom_qty})
        self.write({'autofill_done': True})
