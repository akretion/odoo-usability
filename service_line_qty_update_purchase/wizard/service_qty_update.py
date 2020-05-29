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
        if self._context.get('active_model') == 'purchase.order' and self._context.get('active_id'):
            lines = []
            order = self.env['purchase.order'].browse(self._context['active_id'])
            for l in order.order_line.filtered(lambda x: x.product_id.type == 'service'):
                if float_compare(l.product_qty, l.qty_received, precision_digits=prec) > 0:
                    lines.append((0, 0, {
                        'purchase_line_id': l.id,
                        'product_id': l.product_id.id,
                        'name': l.name,
                        'order_qty': l.product_qty,
                        'pre_delivered_qty': l.qty_received,
                        'uom_id': l.product_uom.id,
                        }))
            if lines:
                res['line_ids'] = lines
            else:
                raise UserError(_(
                    "All service lines are fully received."))
        return res


class ServiceQtyUpdateLine(models.TransientModel):
    _inherit = 'service.qty.update.line'

    purchase_line_id = fields.Many2one('purchase.order.line', string='Purchase Line', readonly=True)

    def process_line(self):
        po_line = self.purchase_line_id
        if po_line:
            po_line.write({'qty_received': self.post_delivered_qty})
            body = """
            <p>Received qty updated on service line <em>%s</em>:
            <ul>
            <li>Added received qty: %s</li>
            <li>Total received qty: %s</li>
            </ul></p>
            """ % (self.added_delivered_qty, self.post_delivered_qty)
            if self.comment:
                body += '<p>Comment: %s</p>' % self.comment
            po_line.order_id.message_post(body=body)
        return super().process_line()
