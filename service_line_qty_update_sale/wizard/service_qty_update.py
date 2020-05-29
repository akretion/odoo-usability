# Copyright 2020 Akretion France (http://www.akretion.com/)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import _, api, fields, models
from odoo.tools import float_compare
from odoo.exceptions import UserError


class ServiceQtyUpdate(models.TransientModel):
    _inherit = 'service.qty.update'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        prec = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        if self._context.get('active_model') == 'sale.order' and self._context.get('active_id'):
            lines = []
            order = self.env['sale.order'].browse(self._context['active_id'])
            for l in order.order_line.filtered(lambda x: x.product_id.type == 'service'):
                if float_compare(l.product_qty, l.qty_delivered, precision_digits=prec) > 0:
                    lines.append((0, 0, {
                        'sale_line_id': l.id,
                        'product_id': l.product_id.id,
                        'name': l.name,
                        'name_readonly': l.name,
                        'order_qty': l.product_uom_qty,
                        'order_qty_readonly': l.product_uom_qty,
                        'pre_delivered_qty': l.qty_delivered,
                        'pre_delivered_qty_readonly': l.qty_delivered,
                        'uom_id': l.product_uom.id,
                        }))
            if lines:
                res['line_ids'] = lines
            else:
                raise UserError(_(
                    "All service lines are fully delivered."))
        return res


class ServiceQtyUpdateLine(models.TransientModel):
    _inherit = 'service.qty.update.line'

    sale_line_id = fields.Many2one('sale.order.line', string='Sale Line', readonly=True)

    def process_line(self):
        so_line = self.sale_line_id
        if so_line:
            new_qty = so_line.qty_delivered + self.added_delivered_qty
            so_line.write({'qty_delivered': new_qty})
            body = """
            <p>Delivered qty updated on service line <b>%s</b>:
            <ul>
            <li>Added delivered qty: <b>%s</b></li>
            <li>Total delivered qty: %s</li>
            </ul></p>
            """ % (self.name, self.added_delivered_qty, new_qty)
            if self.comment:
                body += '<p>Comment: %s</p>' % self.comment
            so_line.order_id.message_post(body=body)
        return super().process_line()
