from odoo import models
from odoo.tools import float_is_zero


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """
        Create as many invoice lines as order lines with their original
        order line taxes. Lines quantities have the ratio of the advance payment.
        """
        invoice_vals = super()._prepare_invoice_values(order, name, amount, so_line)
        lines = []
        uom_precision_digits = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for line in order.order_line:
            if (
                not float_is_zero(
                    # avoids taking lines like previous advance payments
                    line.product_uom_qty, precision_digits=uom_precision_digits
                )
            ):
                lines.append((0, 0, {
                    "name": name,
                    "price_unit": line.price_unit,
                    "quantity": line.product_uom_qty * amount / order.amount_total,
                    "product_id": line.product_id.id,
                    "product_uom_id": line.product_uom.id,
                    "tax_ids": [(6, 0, line.tax_id.ids)],
                    "sale_line_ids": [(6, 0, [line.id])],
                    "analytic_tag_ids": [(6, 0, line.analytic_tag_ids.ids)],
                    "analytic_account_id": order.analytic_account_id.id or False,
                }))
        invoice_vals["invoice_line_ids"] = lines
        return invoice_vals
