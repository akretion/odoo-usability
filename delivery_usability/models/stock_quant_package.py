# Copyright 2019-2024 Akretion France (https://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models
from odoo.tools import float_is_zero


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    # These 2 fields are defined in the 'delivery' module but they forgot
    # the decimal precision
    shipping_weight = fields.Float(digits="Stock Weight")
    weight = fields.Float(digits="Stock Weight")

    # Fixing bug https://github.com/odoo/odoo/issues/34702
    # and take into account the weight of the packaging
    # WARNING: this method _compute_weight() is also inherited by the OCA module
    # base_delivery_carrier_label so if you use that module, you should copy
    # that piece of code in a custom module that depend on delivery_usability
    # and base_delivery_carrier_label
    def _compute_weight(self):
        smlo = self.env["stock.move.line"]
        weight_uom_categ = self.env.ref("uom.product_uom_categ_kgm")
        kg_uom = self.env.ref("uom.product_uom_kgm")
        weight_prec = self.env['decimal.precision'].precision_get('Stock Weight')
        for package in self:
            # if the weight of the package has been measured,
            # it is written in shipping_weight
            if not float_is_zero(package.shipping_weight, precision_digits=weight_prec):
                weight = package.shipping_weight
            # otherwise, we compute the theorical weight from the weight of the products
            # and the weight of the packaging
            # Since Odoo v11, consu products don't create quants, so I can't loop
            # on pack.quant_ids to get all the items inside a package: I have to
            # get the picking, then loop on the stock.move.line of that picking
            # linked to that package
            else:
                weight = 0.0
                # the package can be seen in a return
                # So I get the picking of it's first appearance
                domain = [
                    ("result_package_id", "=", package.id),
                    ("product_id", "!=", False),
                    ]
                first_move_line = smlo.search(
                    domain + [('picking_id', '!=', False)], limit=1, order='id')
                if first_move_line:
                    picking_id = first_move_line.picking_id.id
                    current_picking_move_line_ids = smlo.search(
                        domain + [("picking_id", "=", picking_id)])
                    for ml in current_picking_move_line_ids:
                        if ml.product_uom_id.category_id == weight_uom_categ:
                            weight += ml.product_uom_id._compute_quantity(
                                ml.qty_done, kg_uom
                            )
                        else:
                            weight += (
                                ml.product_uom_id._compute_quantity(
                                    ml.qty_done, ml.product_id.uom_id
                                )
                                * ml.product_id.weight
                            )
                if package.packaging_id:
                    weight += package.packaging_id.weight
            package.weight = weight
